import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { ADMIN_SESSION_COOKIE, verifyAdminSessionToken } from "@/lib/session";
import { listProviders } from "@/lib/providers";
import { getActiveProviderId } from "@/lib/activeProvider";
import { getStats } from "@/lib/stats";
import { LogoutButton } from "@/components/LogoutButton";
import { ActiveProviderControl } from "@/components/ActiveProviderControl";

export default async function AdminPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get(ADMIN_SESSION_COOKIE)?.value;

  if (!verifyAdminSessionToken(session)) {
    redirect("/admin/login");
  }

  const providers = listProviders();
  const activeProviderId = getActiveProviderId();
  const stats = getStats();
  const uptimeMinutes = stats.uptimeMinutes;

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-stone-900 dark:text-stone-100">Admin</h1>
        <LogoutButton />
      </div>

      <section className="mb-8 rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          Provider configuration
        </h2>
        <ul className="divide-y divide-stone-100 dark:divide-stone-800">
          {providers.map((provider) => (
            <li key={provider.id} className="flex items-center justify-between py-2 text-sm">
              <span className="text-stone-700 dark:text-stone-300">{provider.label}</span>
              <span
                className={
                  provider.configured
                    ? "rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400"
                    : "rounded-full bg-stone-100 px-2 py-0.5 text-xs text-stone-500 dark:bg-stone-800 dark:text-stone-400"
                }
              >
                {provider.configured ? "Key configured" : "No key set"}
              </span>
            </li>
          ))}
        </ul>
        <p className="mt-3 text-xs text-stone-400">
          Set API keys as environment variables on the server (see env.template.txt). No key value
          is ever shown here.
        </p>
      </section>

      <section className="mb-8 rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          Active provider
        </h2>
        <ActiveProviderControl providers={providers} activeProviderId={activeProviderId} />
      </section>

      <section className="rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          Session usage
        </h2>
        <p className="text-xs text-stone-400">
          Counts only, reset on server restart. No uploaded image or transcription text is ever
          stored.
        </p>
        <dl className="mt-4 grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
          <div>
            <dt className="text-stone-400">Uptime</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {uptimeMinutes}m
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">Requests</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {stats.totalRequests}
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">Failures</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {stats.totalFailures}
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">By provider</dt>
            <dd className="text-sm text-stone-700 dark:text-stone-300">
              {Object.entries(stats.byProvider)
                .map(([id, count]) => `${id}: ${count}`)
                .join(" · ")}
            </dd>
          </div>
        </dl>
      </section>
    </div>
  );
}
