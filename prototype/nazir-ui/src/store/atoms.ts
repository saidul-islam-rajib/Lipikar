import { atom } from "jotai";
import type { ProviderId, ProviderInfo, TranscriptionResult } from "@/lib/providers/types";

export interface UploadedImage {
  fileName: string;
  mimeType: string;
  base64: string;
  previewUrl: string;
}

export type RequestStatus = "idle" | "loading" | "error" | "done";

export const providersAtom = atom<ProviderInfo[]>([]);
export const selectedProviderAtom = atom<ProviderId>("claude");
export const uploadedImageAtom = atom<UploadedImage | null>(null);
export const resultAtom = atom<TranscriptionResult | null>(null);
export const statusAtom = atom<RequestStatus>("idle");
export const errorMessageAtom = atom<string | null>(null);
