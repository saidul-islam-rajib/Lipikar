import Link from "next/link";
import { Logo } from "./Logo";

export function Header() {
  return (
    <header className="border-b border-stone-200 bg-white/80 backdrop-blur dark:border-stone-800 dark:bg-stone-950/80">
      <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <Logo />
          <div>
            <p className="text-base font-semibold text-stone-900 dark:text-stone-100">Lipikar</p>
            <p className="text-xs text-stone-500 dark:text-stone-400">
              দলিল transcription prototype
            </p>
          </div>
        </Link>
        <Link
          href="/admin"
          className="text-sm text-stone-500 transition hover:text-stone-900 dark:text-stone-400 dark:hover:text-stone-100"
        >
          Admin
        </Link>
      </div>
    </header>
  );
}
