"use client";

import { Provider } from "jotai";
import type { ReactNode } from "react";

export function JotaiRoot({ children }: { children: ReactNode }) {
  return <Provider>{children}</Provider>;
}
