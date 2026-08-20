import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { z } from "zod";
import { ADMIN_SESSION_COOKIE, verifyAdminSessionToken } from "@/lib/session";
import { getProvider } from "@/lib/providers";
import { getActiveProviderId, setActiveProviderId } from "@/lib/activeProvider";
import type { ProviderId } from "@/lib/providers/types";
import { strings } from "@/lib/strings";

const bodySchema = z.object({
  providerId: z.enum(["claude", "openai", "gemini"] satisfies readonly ProviderId[]),
});

async function requireAdmin(): Promise<boolean> {
  const cookieStore = await cookies();
  return verifyAdminSessionToken(cookieStore.get(ADMIN_SESSION_COOKIE)?.value);
}

export async function GET() {
  return NextResponse.json({ activeProviderId: getActiveProviderId() });
}

export async function POST(request: Request) {
  if (!(await requireAdmin())) {
    return NextResponse.json({ error: strings.api.notSignedIn }, { status: 401 });
  }

  const body = await request.json().catch(() => null);
  const parsed = bodySchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: strings.api.providerIdRequired }, { status: 400 });
  }

  const provider = getProvider(parsed.data.providerId);
  if (!provider.isConfigured()) {
    return NextResponse.json(
      { error: strings.api.cannotActivateUnconfigured(provider.label) },
      { status: 400 },
    );
  }

  setActiveProviderId(provider.id);
  return NextResponse.json({ activeProviderId: getActiveProviderId() });
}
