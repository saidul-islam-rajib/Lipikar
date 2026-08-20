import { strings } from "@/lib/strings";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-stone-200 py-6 dark:border-stone-800">
      <div className="mx-auto max-w-3xl px-6 text-xs text-stone-400 dark:text-stone-500">
        {strings.footer.notice}
      </div>
    </footer>
  );
}
