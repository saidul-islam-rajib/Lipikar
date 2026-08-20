"use client";

import { useState } from "react";
import { useAtomValue } from "jotai";
import { errorMessageAtom, resultAtom, statusAtom } from "@/store/atoms";
import { AssistiveNotice } from "./AssistiveNotice";
import { strings } from "@/lib/strings";

export function ResultCard() {
  const result = useAtomValue(resultAtom);
  const status = useAtomValue(statusAtom);
  const error = useAtomValue(errorMessageAtom);
  const [copied, setCopied] = useState(false);

  if (status === "idle") return null;

  if (status === "error") {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
        {error ?? strings.result.genericError}
      </div>
    );
  }

  if (status === "loading") {
    return (
      <div className="rounded-xl border border-stone-200 bg-white p-6 text-sm text-stone-500 dark:border-stone-800 dark:bg-stone-900">
        {strings.result.reading}
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="space-y-3">
      <AssistiveNotice />
      <div className="rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-xs uppercase tracking-wide text-stone-400">
            {strings.result.draftLabel(result.modelId)}
          </p>
          <button
            type="button"
            onClick={() => {
              void navigator.clipboard.writeText(result.text);
              setCopied(true);
              setTimeout(() => setCopied(false), 1500);
            }}
            className="text-xs text-stone-500 hover:text-stone-800 dark:text-stone-400 dark:hover:text-stone-100"
          >
            {copied ? strings.result.copied : strings.result.copy}
          </button>
        </div>
        <p className="whitespace-pre-wrap font-bengali text-base leading-relaxed text-stone-900 dark:text-stone-100">
          {result.text || strings.result.empty}
        </p>
      </div>
    </div>
  );
}
