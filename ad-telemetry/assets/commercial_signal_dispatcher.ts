import type { CommercialSignal } from '@astrobranding/contracts';

/**
 * Normalizes email address according to Meta and Google Ads Enhanced Conversions rules.
 * Lowers case, trims whitespace, removes dots for gmail, removes + aliases.
 */
export async function hashSha256(input: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(input);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function normalizeEmail(email: string): string {
  let [local, domain] = email.trim().toLowerCase().split('@');
  if (!domain) return email.trim().toLowerCase();
  if (domain === 'gmail.com' || domain === 'googlemail.com') {
    local = local.replace(/\./g, '').split('+')[0];
  }
  return `${local}@${domain}`;
}

export function normalizePhone(phone: string): string {
  return phone.replace(/[^\d+]/g, '');
}

/**
 * Dispatches a commercial signal to browser pixels (Meta Pixel, Google Tag, TikTok Pixel)
 * with a shared event_id for deduplication against server CAPI.
 */
export function dispatchBrowserSignal(signal: CommercialSignal): void {
  if (typeof window === 'undefined') return;

  // 1. Meta Pixel
  if (typeof (window as any).fbq === 'function') {
    const metaEventName = signal.event_name;
    const metaPayload: Record<string, unknown> = {
      content_type: signal.content_type,
      currency: signal.currency,
      value: signal.value,
      ...signal.custom_data,
    };
    (window as any).fbq('track', metaEventName, metaPayload, { eventID: signal.event_id });
  }

  // 2. Google Tag (gtag)
  if (typeof (window as any).gtag === 'function') {
    (window as any).gtag('event', signal.event_name.toLowerCase(), {
      transaction_id: signal.event_id,
      value: signal.value,
      currency: signal.currency,
      ...signal.custom_data,
    });
  }

  // 3. TikTok Pixel (ttq)
  if (typeof (window as any).ttq === 'object' && typeof (window as any).ttq.track === 'function') {
    (window as any).ttq.track(signal.event_name, {
      content_type: signal.content_type,
      value: signal.value,
      currency: signal.currency,
      ...signal.custom_data,
    }, {
      event_id: signal.event_id,
    });
  }
}
