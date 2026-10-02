import crypto from "node:crypto";

/**
 * Lua script for atomic lock release.
 * Verifies that the lock value matches the caller's owner token before deleting.
 */
const UNLOCK_LUA_SCRIPT = `
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])
else
  return 0
end
`;

export interface LockResult {
  acquired: boolean;
  ownerToken?: string;
  lockKey: string;
}

/**
 * Acquires a distributed lock in Valkey/Redis using a cryptographically unique token.
 */
export async function acquireLock(
  valkey: any,
  resourceId: string,
  ttlSeconds: number = 60,
  keyPrefix: string = "lock:payment:"
): Promise<LockResult> {
  const lockKey = `${keyPrefix}${resourceId}`;
  const ownerToken = crypto.randomUUID();

  // Atomically set key only if it does not exist (NX) with expiration (EX)
  const result = await valkey.set(lockKey, ownerToken, "EX", ttlSeconds, "NX");
  const acquired = result === "OK" || result === true || result === 1;

  return {
    acquired,
    ownerToken: acquired ? ownerToken : undefined,
    lockKey
  };
}

/**
 * Releases a distributed lock atomically using a Lua script to prevent deleting
 * a lock that has expired and been acquired by another process.
 */
export async function releaseLock(
  valkey: any,
  lockKey: string,
  ownerToken: string
): Promise<boolean> {
  try {
    const result = await valkey.eval(UNLOCK_LUA_SCRIPT, 1, lockKey, ownerToken);
    return result === 1;
  } catch (error) {
    console.error(`[valkey-lock] Failed to release lock ${lockKey}:`, error);
    return false;
  }
}

/**
 * Higher-order helper to execute a critical section within an atomic distributed lock.
 */
export async function withDistributedLock<T>(
  valkey: any,
  resourceId: string,
  ttlSeconds: number,
  criticalSection: () => Promise<T>,
  keyPrefix: string = "lock:payment:"
): Promise<{ executed: boolean; result?: T; reason?: string }> {
  const lock = await acquireLock(valkey, resourceId, ttlSeconds, keyPrefix);
  if (!lock.acquired || !lock.ownerToken) {
    return { executed: false, reason: "LOCK_ACQUISITION_FAILED" };
  }

  try {
    const result = await criticalSection();
    return { executed: true, result };
  } finally {
    await releaseLock(valkey, lock.lockKey, lock.ownerToken);
  }
}
