"use client";

import { useEffect } from "react";
import { useAtom } from "jotai";
import { providersAtom, selectedProviderAtom } from "@/store/atoms";
import { strings } from "@/lib/strings";

export function ProviderSelect() {
  const [providers, setProviders] = useAtom(providersAtom);
  const [selected, setSelected] = useAtom(selectedProviderAtom);

  useEffect(() => {
    let cancelled = false;

    fetch("/api/providers")
      .then((res) => res.json())
      .then((data: { providers: typeof providers; defaultProviderId: typeof selected }) => {
        if (cancelled) return;
        setProviders(data.providers);
        setSelected(data.defaultProviderId);
      })
      .catch(() => {
        if (!cancelled) setProviders([]);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <label className="mb-2 block text-sm font-medium text-stone-700 dark:text-stone-300">
        {strings.providerSelect.label}
      </label>
      <div className="flex flex-wrap gap-2">
        {providers.map((provider) => (
          <button
            key={provider.id}
            type="button"
            disabled={!provider.configured}
            onClick={() => setSelected(provider.id)}
            title={provider.configured ? undefined : strings.providerSelect.unconfiguredHint}
            className={`rounded-full border px-4 py-1.5 text-sm transition ${
              selected === provider.id
                ? "border-stone-900 bg-stone-900 text-white dark:border-stone-100 dark:bg-stone-100 dark:text-stone-900"
                : "border-stone-300 text-stone-600 hover:border-stone-400 dark:border-stone-700 dark:text-stone-400"
            } ${!provider.configured ? "cursor-not-allowed opacity-40" : ""}`}
          >
            {provider.label}
          </button>
        ))}
        {providers.length === 0 && (
          <p className="text-sm text-stone-400">{strings.providerSelect.loading}</p>
        )}
      </div>
    </div>
  );
}
