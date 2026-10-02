export type CircuitState = "CLOSED" | "OPEN" | "HALF_OPEN";

export interface CircuitBreakerOptions {
  failureThreshold: number; // e.g. 5 failures
  cooldownPeriodMs: number; // e.g. 30000 ms before entering HALF_OPEN
  halfOpenMaxSuccesses: number; // e.g. 2 successful executions to close
}

export class CircuitBreaker {
  private state: CircuitState = "CLOSED";
  private failureCount = 0;
  private successCount = 0;
  private nextAttempt = 0;
  private options: CircuitBreakerOptions;

  constructor(options?: Partial<CircuitBreakerOptions>) {
    this.options = {
      failureThreshold: options?.failureThreshold ?? 5,
      cooldownPeriodMs: options?.cooldownPeriodMs ?? 30000,
      halfOpenMaxSuccesses: options?.halfOpenMaxSuccesses ?? 2
    };
  }

  getState(): CircuitState {
    if (this.state === "OPEN" && Date.now() >= this.nextAttempt) {
      this.state = "HALF_OPEN";
      this.successCount = 0;
    }
    return this.state;
  }

  async execute<T>(action: () => Promise<T>): Promise<T> {
    const currentState = this.getState();

    if (currentState === "OPEN") {
      throw new Error(`CircuitBreaker is OPEN. Operation rejected. Next attempt at ${new Date(this.nextAttempt).toISOString()}`);
    }

    try {
      const result = await action();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    if (this.state === "HALF_OPEN") {
      this.successCount++;
      if (this.successCount >= this.options.halfOpenMaxSuccesses) {
        this.state = "CLOSED";
        this.failureCount = 0;
        this.successCount = 0;
      }
    } else if (this.state === "CLOSED") {
      this.failureCount = 0;
    }
  }

  private onFailure() {
    this.failureCount++;
    if (this.state === "HALF_OPEN" || this.failureCount >= this.options.failureThreshold) {
      this.state = "OPEN";
      this.nextAttempt = Date.now() + this.options.cooldownPeriodMs;
    }
  }
}
