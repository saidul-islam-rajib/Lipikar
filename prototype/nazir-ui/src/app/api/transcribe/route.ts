import { NextResponse } from "next/server";
import { z } from "zod";
import { getProvider } from "@/lib/providers";
import type { ProviderId } from "@/lib/providers/types";
import { recordFailure, recordRequest } from "@/lib/stats";

const MAX_IMAGE_BYTES = 8 * 1024 * 1024;
const MAX_BASE64_LENGTH = Math.ceil(MAX_IMAGE_BYTES / 3) * 4;

const ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"] as const;

const requestSchema = z.object({
  providerId: z.enum(["claude", "openai", "gemini"] satisfies readonly ProviderId[]),
  mimeType: z.enum(ALLOWED_MIME_TYPES),
  imageBase64: z.string().min(1).max(MAX_BASE64_LENGTH),
});

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = requestSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Invalid request. Expected providerId, mimeType, and imageBase64 (max 8MB)." },
      { status: 400 },
    );
  }

  const { providerId, mimeType, imageBase64 } = parsed.data;
  const provider = getProvider(providerId);

  if (!provider.isConfigured()) {
    return NextResponse.json(
      { error: `${provider.label} is not configured on this server. Set its API key in .env.local.` },
      { status: 503 },
    );
  }

  try {
    const result = await provider.transcribe(imageBase64, mimeType);
    recordRequest(providerId);
    return NextResponse.json({ result });
  } catch (error) {
    recordFailure();
    const message = error instanceof Error ? error.message : "Transcription failed.";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
