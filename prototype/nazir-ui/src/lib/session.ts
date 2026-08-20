import { createHmac, timingSafeEqual } from "crypto";

export const ADMIN_SESSION_COOKIE = "nazir_admin_session";
export const ADMIN_SESSION_MAX_AGE_SECONDS = 60 * 60 * 12;

interface SessionPayload {
  role: "admin";
  issuedAt: number;
}

function sessionSecret(): string {
  const secret = process.env.SESSION_SECRET;
  if (!secret) {
    throw new Error("SESSION_SECRET is not set. Add it to .env.local before starting the server.");
  }
  return secret;
}

function sign(payload: string): string {
  return createHmac("sha256", sessionSecret()).update(payload).digest("base64url");
}

export function createAdminSessionToken(): string {
  const payload: SessionPayload = { role: "admin", issuedAt: Date.now() };
  const encoded = Buffer.from(JSON.stringify(payload)).toString("base64url");
  return `${encoded}.${sign(encoded)}`;
}

export function verifyAdminSessionToken(token: string | undefined | null): boolean {
  if (!token) return false;

  const [encoded, signature] = token.split(".");
  if (!encoded || !signature) return false;

  const expectedSignature = sign(encoded);
  const provided = Buffer.from(signature);
  const expected = Buffer.from(expectedSignature);
  if (provided.length !== expected.length || !timingSafeEqual(provided, expected)) {
    return false;
  }

  try {
    const payload = JSON.parse(Buffer.from(encoded, "base64url").toString()) as SessionPayload;
    const ageSeconds = (Date.now() - payload.issuedAt) / 1000;
    return payload.role === "admin" && ageSeconds >= 0 && ageSeconds < ADMIN_SESSION_MAX_AGE_SECONDS;
  } catch {
    return false;
  }
}
