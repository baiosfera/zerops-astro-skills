import type { AttributionSession, AttributionTouch } from '@astrobranding/contracts';

const COOKIE_NAME = '__attr_session';
const COOKIE_MAX_AGE_DAYS = 90;

export function getRootDomain(hostname = window.location.hostname): string {
  const parts = hostname.split('.');
  if (parts.length <= 2) return `.${hostname}`;
  return `.${parts.slice(-2).join('.')}`;
}

export function parseAttributionCookie(): AttributionSession | null {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp(`(^|;\\s*)${COOKIE_NAME}=([^;]*)`));
  if (!match) return null;
  try {
    return JSON.parse(decodeURIComponent(match[2])) as AttributionSession;
  } catch {
    return null;
  }
}

export function persistAttributionCookie(session: AttributionSession): void {
  if (typeof document === 'undefined') return;
  const domain = getRootDomain();
  const maxAgeSeconds = COOKIE_MAX_AGE_DAYS * 86400;
  const serialized = encodeURIComponent(JSON.stringify(session));
  document.cookie = `${COOKIE_NAME}=${serialized}; Domain=${domain}; Path=/; Max-Age=${maxAgeSeconds}; SameSite=Lax; Secure`;
}

export function initAttributionTracker(): AttributionSession {
  if (typeof window === 'undefined') {
    throw new Error('initAttributionTracker must be invoked in the browser runtime.');
  }

  const now = Date.now();
  const urlParams = new URLSearchParams(window.location.search);
  let session = parseAttributionCookie();

  if (!session) {
    session = {
      client_id: crypto.randomUUID(),
      first_touch: {
        timestamp: now,
        landing_url: window.location.href,
        referrer: document.referrer || '',
      },
      last_touch: {
        timestamp: now,
        landing_url: window.location.href,
        referrer: document.referrer || '',
      },
    };
  }

  // Meta fbp initialization (fb.1.<ts>.<random>)
  if (!session.fbp) {
    session.fbp = `fb.1.${now}.${Math.floor(Math.random() * 8999999999 + 1000000000)}`;
  }

  // Meta fbc initialization: Must format fb.1.<ts>.<fbclid>
  const fbclid = urlParams.get('fbclid');
  if (fbclid) {
    session.fbc = `fb.1.${now}.${fbclid}`;
  }

  // Check if current pageview carries new attribution parameters
  const attributionKeys = [
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'gclid', 'gbraid', 'wbraid', 'fbclid', 'ttclid', 'msclkid'
  ];
  const hasParams = attributionKeys.some((k) => urlParams.has(k));

  if (hasParams || !session.last_touch.landing_url) {
    const currentTouch: AttributionTouch = {
      timestamp: now,
      landing_url: window.location.href,
      referrer: document.referrer || '',
      utm_source: urlParams.get('utm_source') || undefined,
      utm_medium: urlParams.get('utm_medium') || undefined,
      utm_campaign: urlParams.get('utm_campaign') || undefined,
      utm_term: urlParams.get('utm_term') || undefined,
      utm_content: urlParams.get('utm_content') || undefined,
      gclid: urlParams.get('gclid') || undefined,
      gbraid: urlParams.get('gbraid') || undefined,
      wbraid: urlParams.get('wbraid') || undefined,
      fbclid: fbclid || undefined,
      ttclid: urlParams.get('ttclid') || undefined,
      msclkid: urlParams.get('msclkid') || undefined,
    };

    if (!session.first_touch.utm_source && currentTouch.utm_source) {
      session.first_touch = currentTouch;
    }
    session.last_touch = currentTouch;
  }

  persistAttributionCookie(session);
  return session;
}
