import { strings } from "@/lib/strings";

export function AssistiveNotice() {
  return (
    <div className="rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-200">
      <p className="font-medium">{strings.assistiveNotice.heading}</p>
      <p className="mt-1">{strings.assistiveNotice.body}</p>
    </div>
  );
}
