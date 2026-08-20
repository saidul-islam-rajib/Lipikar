"use client";

import { useRouter } from "next/navigation";

export function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/admin/logout", { method: "POST" });
    router.push("/admin/login");
    router.refresh();
  }

  return (
    <button
      type="button"
      onClick={() => void handleLogout()}
      className="text-sm text-stone-500 hover:text-stone-800 dark:text-stone-400 dark:hover:text-stone-100"
    >
      Sign out
    </button>
  );
}
