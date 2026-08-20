import type { ProviderId } from "./providers/types";

const VALID_IDS: readonly ProviderId[] = ["claude", "openai", "gemini"];

function envDefault(): ProviderId {
  const configured = process.env.DEFAULT_PROVIDER as ProviderId | undefined;
  return configured && VALID_IDS.includes(configured) ? configured : "claude";
}

let activeProviderId: ProviderId = envDefault();

export function getActiveProviderId(): ProviderId {
  return activeProviderId;
}

export function setActiveProviderId(id: ProviderId): void {
  activeProviderId = id;
}
