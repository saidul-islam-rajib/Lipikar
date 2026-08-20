import { NextResponse } from "next/server";
import { listProviders } from "@/lib/providers";
import { getActiveProviderId } from "@/lib/activeProvider";

export async function GET() {
  return NextResponse.json({
    providers: listProviders(),
    defaultProviderId: getActiveProviderId(),
  });
}
