import { strings } from "@/lib/strings";

export function Logo({ size = 36 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role="img"
      aria-label={strings.header.appName}
      className="shrink-0"
    >
      <rect width="64" height="64" rx="16" fill="#1c1917" />
      <path
        d="M20 46V18h6v22.5h16V46H20Z"
        fill="#fdf6e3"
      />
      <circle cx="46" cy="20" r="4.5" fill="#d97706" />
    </svg>
  );
}
