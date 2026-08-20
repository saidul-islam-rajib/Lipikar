import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { z } from "zod";
import { ADMIN_SESSION_COOKIE, verifyAdminSessionToken } from "@/lib/session";
import { getEffectiveModel, setModelOverride } from "@/lib/modelOverrides";
import { strings } from "@/lib/strings";
import type { ProviderId } from "@/lib/providers/types";

const bodySchema = z.object({
  providerId: z.enum(["claude", "openai", "gemini"] satisfies readonly ProviderId[]),
  modelId: z.string().max(200),
});

export async function POST(request: Request) {
  const cookieStore = await cookies();
  if (!verifyAdminSessionToken(cookieStore.get(ADMIN_SESSION_COOKIE)?.value)) {
    return NextResponse.json({ error: strings.api.notSignedIn }, { status: 401 });
  }

  const body = await request.json().catch(() => null);
  const parsed = bodySchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: strings.api.modelIdRequired }, { status: 400 });
  }

  setModelOverride(parsed.data.providerId, parsed.data.modelId);
  return NextResponse.json({ modelId: getEffectiveModel(parsed.data.providerId) });
}
