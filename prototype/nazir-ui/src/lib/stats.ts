import type { ProviderId } from "./providers/types";

interface RequestStats {
  startedAt: number;
  totalRequests: number;
  totalFailures: number;
  byProvider: Record<ProviderId, number>;
}

const stats: RequestStats = {
  startedAt: Date.now(),
  totalRequests: 0,
  totalFailures: 0,
  byProvider: { claude: 0, openai: 0, gemini: 0 },
};

export function recordRequest(providerId: ProviderId): void {
  stats.totalRequests += 1;
  stats.byProvider[providerId] += 1;
}

export function recordFailure(): void {
  stats.totalFailures += 1;
}

export function getStats(): RequestStats & { uptimeMinutes: number } {
  return {
    ...stats,
    byProvider: { ...stats.byProvider },
    uptimeMinutes: Math.floor((Date.now() - stats.startedAt) / 60000),
  };
}
