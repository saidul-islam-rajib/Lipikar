export function AssistiveNotice() {
  return (
    <div className="rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-200">
      <p className="font-medium">This is a prototype, not the trained Lipikar pipeline.</p>
      <p className="mt-1">
        Transcriptions come from a general-purpose AI model, not a model trained on Bengali deed
        handwriting. Treat every result as a rough draft that a human must verify against the
        original document — never rely on it for a legal purpose.
      </p>
    </div>
  );
}
