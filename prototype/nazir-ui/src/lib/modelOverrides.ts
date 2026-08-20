import type { ProviderId } from "./providers/types";

const ENV_VAR: Record<ProviderId, string> = {
  claude: "ANTHROPIC_MODEL",
  openai: "OPENAI_MODEL",
  gemini: "GEMINI_MODEL",
};

const BUILTIN_DEFAULT: Record<ProviderId, string> = {
  claude: "claude-sonnet-5",
  openai: "gpt-4o",
  gemini: "gemini-3.6-flash",
};

const overrides: Partial<Record<ProviderId, string>> = {};

export function getEffectiveModel(providerId: ProviderId): string {
  return overrides[providerId] || process.env[ENV_VAR[providerId]] || BUILTIN_DEFAULT[providerId];
}

export function hasModelOverride(providerId: ProviderId): boolean {
  return providerId in overrides;
}

export function setModelOverride(providerId: ProviderId, modelId: string): void {
  const trimmed = modelId.trim();
  if (trimmed) {
    overrides[providerId] = trimmed;
  } else {
    delete overrides[providerId];
  }
}
