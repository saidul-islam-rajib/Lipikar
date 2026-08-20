import type { ProviderId, ProviderInfo, VisionProvider } from "./types";
import { claudeProvider } from "./claude";
import { openaiProvider } from "./openai";
import { geminiProvider } from "./gemini";

const registry: Record<ProviderId, VisionProvider> = {
  claude: claudeProvider,
  openai: openaiProvider,
  gemini: geminiProvider,
};

export function listProviders(): ProviderInfo[] {
  return Object.values(registry).map((provider) => ({
    id: provider.id,
    label: provider.label,
    configured: provider.isConfigured(),
  }));
}

export function getProvider(id: ProviderId): VisionProvider {
  return registry[id];
}

export type { ProviderId, ProviderInfo, TranscriptionResult, VisionProvider } from "./types";
