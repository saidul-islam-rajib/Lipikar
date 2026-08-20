import { NextResponse } from "next/server";
import { listProviders, defaultProviderId } from "@/lib/providers";

export async function GET() {
  return NextResponse.json({
    providers: listProviders(),
    defaultProviderId: defaultProviderId(),
  });
}
