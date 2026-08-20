import { ProviderSelect } from "@/components/ProviderSelect";
import { UploadCard } from "@/components/UploadCard";
import { ResultCard } from "@/components/ResultCard";
import { strings } from "@/lib/strings";

export default function Home() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-stone-900 dark:text-stone-100">
          {strings.home.heading}
        </h1>
        <p className="mt-2 text-sm text-stone-500 dark:text-stone-400">
          {strings.home.subheading}
        </p>
      </div>

      <div className="space-y-6">
        <ProviderSelect />
        <UploadCard />
        <ResultCard />
      </div>
    </div>
  );
}
