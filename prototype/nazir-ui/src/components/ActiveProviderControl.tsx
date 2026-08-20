"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { ProviderId, ProviderInfo } from "@/lib/providers/types";

export function ActiveProviderControl({
  providers,
  activeProviderId,
}: {
  providers: ProviderInfo[];
  activeProviderId: ProviderId;
}) {
  const router = useRouter();
  const [pending, setPending] = useState<ProviderId | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function activate(providerId: ProviderId) {
    if (providerId === activeProviderId) return;
    setPending(providerId);
    setError(null);

    try {
      const response = await fetch("/api/admin/active-provider", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ providerId }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? "Could not change the active provider.");
      }

      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not change the active provider.");
    } finally {
      setPending(null);
    }
  }

  return (
    <div>
      <p className="mb-2 text-xs text-stone-400">
        Only one provider is active at a time. The active provider is what the public upload page
        uses by default.
      </p>
      <div className="flex flex-wrap gap-2">
        {providers.map((provider) => {
          const isActive = provider.id === activeProviderId;
          return (
            <button
              key={provider.id}
              type="button"
              disabled={!provider.configured || pending !== null}
              onClick={() => void activate(provider.id)}
              title={provider.configured ? undefined : "No API key configured on the server"}
              className={`rounded-full border px-4 py-1.5 text-sm transition ${
                isActive
                  ? "border-emerald-600 bg-emerald-600 text-white"
                  : "border-stone-300 text-stone-600 hover:border-stone-400 dark:border-stone-700 dark:text-stone-400"
              } ${!provider.configured ? "cursor-not-allowed opacity-40" : ""} ${
                pending === provider.id ? "opacity-60" : ""
              }`}
            >
              {isActive ? "● " : ""}
              {provider.label}
            </button>
          );
        })}
      </div>
      {error && <p className="mt-2 text-sm text-red-600 dark:text-red-400">{error}</p>}
    </div>
  );
}
