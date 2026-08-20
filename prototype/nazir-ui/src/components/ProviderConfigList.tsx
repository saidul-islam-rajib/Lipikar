"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { ProviderId } from "@/lib/providers/types";
import { strings } from "@/lib/strings";

export interface ProviderConfigRow {
  id: ProviderId;
  label: string;
  configured: boolean;
  model: string;
  isOverridden: boolean;
}

export function ProviderConfigList({ rows }: { rows: ProviderConfigRow[] }) {
  const router = useRouter();
  const [drafts, setDrafts] = useState<Record<string, string>>(
    Object.fromEntries(rows.map((row) => [row.id, row.model])),
  );
  const [pending, setPending] = useState<ProviderId | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function save(providerId: ProviderId, modelId: string) {
    setPending(providerId);
    setError(null);

    try {
      const response = await fetch("/api/admin/model", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ providerId, modelId }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? strings.admin.modelGenericError);
      }

      setDrafts((d) => ({ ...d, [providerId]: data.modelId }));
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : strings.admin.modelGenericError);
    } finally {
      setPending(null);
    }
  }

  return (
    <div>
      <ul className="divide-y divide-stone-100 dark:divide-stone-800">
        {rows.map((row) => (
          <li key={row.id} className="py-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-stone-700 dark:text-stone-300">{row.label}</span>
              <span
                className={
                  row.configured
                    ? "rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400"
                    : "rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-500 dark:bg-stone-800 dark:text-stone-400"
                }
              >
                {row.configured ? strings.admin.keyConfigured : strings.admin.noKeySet}
              </span>
            </div>
            <div className="mt-2 flex items-center gap-2">
              <label htmlFor={`model-${row.id}`} className="sr-only">
                {strings.admin.modelLabel}
              </label>
              <input
                id={`model-${row.id}`}
                value={drafts[row.id]}
                onChange={(e) => setDrafts((d) => ({ ...d, [row.id]: e.target.value }))}
                className="flex-1 rounded-lg border border-stone-300 px-2 py-1 text-xs text-stone-700 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300"
              />
              <button
                type="button"
                disabled={pending !== null || drafts[row.id] === row.model}
                onClick={() => void save(row.id, drafts[row.id])}
                className="rounded-lg border border-stone-300 px-3 py-1 text-xs text-stone-600 transition hover:border-stone-400 disabled:cursor-not-allowed disabled:opacity-40 dark:border-stone-700 dark:text-stone-400"
              >
                {strings.admin.modelSave}
              </button>
              {row.isOverridden && (
                <button
                  type="button"
                  disabled={pending !== null}
                  onClick={() => void save(row.id, "")}
                  className="text-xs text-stone-400 hover:text-stone-700 dark:hover:text-stone-200"
                >
                  {strings.admin.modelReset}
                </button>
              )}
              {row.isOverridden && (
                <span className="text-xs text-amber-600 dark:text-amber-400">
                  {strings.admin.modelOverridden}
                </span>
              )}
            </div>
          </li>
        ))}
      </ul>
      <p className="mt-3 text-xs text-stone-400">{strings.admin.keyHint}</p>
      {error && <p className="mt-2 text-sm text-red-600 dark:text-red-400">{error}</p>}
    </div>
  );
}
