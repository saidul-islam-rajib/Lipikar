import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { ADMIN_SESSION_COOKIE, verifyAdminSessionToken } from "@/lib/session";
import { listProviders } from "@/lib/providers";
import { getActiveProviderId } from "@/lib/activeProvider";
import { getEffectiveModel, hasModelOverride } from "@/lib/modelOverrides";
import { getStats } from "@/lib/stats";
import { LogoutButton } from "@/components/LogoutButton";
import { ActiveProviderControl } from "@/components/ActiveProviderControl";
import { ProviderConfigList } from "@/components/ProviderConfigList";
import { strings } from "@/lib/strings";

export default async function AdminPage() {
  const cookieStore = await cookies();
  const session = cookieStore.get(ADMIN_SESSION_COOKIE)?.value;

  if (!verifyAdminSessionToken(session)) {
    redirect("/admin/login");
  }

  const providers = listProviders();
  const activeProviderId = getActiveProviderId();
  const providerRows = providers.map((provider) => ({
    ...provider,
    model: getEffectiveModel(provider.id),
    isOverridden: hasModelOverride(provider.id),
  }));
  const stats = getStats();
  const uptimeMinutes = stats.uptimeMinutes;

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-stone-900 dark:text-stone-100">
          {strings.admin.heading}
        </h1>
        <LogoutButton />
      </div>

      <section className="mb-8 rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          {strings.admin.providerConfigHeading}
        </h2>
        <ProviderConfigList rows={providerRows} />
      </section>

      <section className="mb-8 rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          {strings.admin.activeProviderHeading}
        </h2>
        <ActiveProviderControl providers={providers} activeProviderId={activeProviderId} />
      </section>

      <section className="rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
        <h2 className="mb-4 text-sm font-medium uppercase tracking-wide text-stone-400">
          {strings.admin.sessionUsageHeading}
        </h2>
        <p className="text-xs text-stone-400">{strings.admin.sessionUsageHint}</p>
        <dl className="mt-4 grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
          <div>
            <dt className="text-stone-400">{strings.admin.uptime}</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {uptimeMinutes}m
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">{strings.admin.requests}</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {stats.totalRequests}
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">{strings.admin.failures}</dt>
            <dd className="text-lg font-semibold text-stone-900 dark:text-stone-100">
              {stats.totalFailures}
            </dd>
          </div>
          <div>
            <dt className="text-stone-400">{strings.admin.byProvider}</dt>
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
