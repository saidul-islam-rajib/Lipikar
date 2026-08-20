"use client";

import { useRef, useState } from "react";
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import {
  errorMessageAtom,
  resultAtom,
  selectedProviderAtom,
  statusAtom,
  uploadedImageAtom,
} from "@/store/atoms";

const MAX_FILE_BYTES = 8 * 1024 * 1024;
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];

function readFileAsBase64(file: File): Promise<{ base64: string; previewUrl: string }> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(reader.error);
    reader.onload = () => {
      const dataUrl = reader.result as string;
      const base64 = dataUrl.split(",")[1] ?? "";
      resolve({ base64, previewUrl: dataUrl });
    };
    reader.readAsDataURL(file);
  });
}

export function UploadCard() {
  const [image, setImage] = useAtom(uploadedImageAtom);
  const selectedProvider = useAtomValue(selectedProviderAtom);
  const setResult = useSetAtom(resultAtom);
  const setStatus = useSetAtom(statusAtom);
  const setError = useSetAtom(errorMessageAtom);
  const status = useAtomValue(statusAtom);
  const [localError, setLocalError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File | undefined) {
    setLocalError(null);
    if (!file) return;

    if (!ACCEPTED_TYPES.includes(file.type)) {
      setLocalError("Please choose a JPEG, PNG, WebP, or GIF image.");
      return;
    }
    if (file.size > MAX_FILE_BYTES) {
      setLocalError("Image is larger than 8MB. Please choose a smaller photo.");
      return;
    }

    const { base64, previewUrl } = await readFileAsBase64(file);
    setImage({ fileName: file.name, mimeType: file.type, base64, previewUrl });
    setResult(null);
    setError(null);
    setStatus("idle");
  }

  async function handleTranscribe() {
    if (!image) return;
    setStatus("loading");
    setError(null);

    try {
      const response = await fetch("/api/transcribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          providerId: selectedProvider,
          mimeType: image.mimeType,
          imageBase64: image.base64,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? "Transcription failed.");
      }

      setResult(data.result);
      setStatus("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Transcription failed.");
      setStatus("error");
    }
  }

  function clearImage() {
    setImage(null);
    setResult(null);
    setError(null);
    setStatus("idle");
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="rounded-xl border border-stone-200 bg-white p-6 dark:border-stone-800 dark:bg-stone-900">
      <label
        htmlFor="deed-photo"
        className="flex min-h-40 cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-stone-300 px-4 py-8 text-center transition hover:border-stone-400 dark:border-stone-700"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          void handleFile(e.dataTransfer.files?.[0]);
        }}
      >
        {image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={image.previewUrl}
            alt="Selected deed photo"
            className="max-h-64 rounded-md object-contain"
          />
        ) : (
          <>
            <p className="text-sm font-medium text-stone-700 dark:text-stone-300">
              Click to choose a photo, or drag one here
            </p>
            <p className="text-xs text-stone-400">JPEG, PNG, WebP, or GIF · up to 8MB</p>
          </>
        )}
        <input
          ref={inputRef}
          id="deed-photo"
          type="file"
          accept={ACCEPTED_TYPES.join(",")}
          className="hidden"
          onChange={(e) => void handleFile(e.target.files?.[0])}
        />
      </label>

      {localError && <p className="mt-3 text-sm text-red-600 dark:text-red-400">{localError}</p>}

      <div className="mt-4 flex items-center gap-3">
        <button
          type="button"
          onClick={handleTranscribe}
          disabled={!image || status === "loading"}
          className="rounded-lg bg-stone-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-stone-700 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-white"
        >
          {status === "loading" ? "Transcribing…" : "Transcribe"}
        </button>
        {image && (
          <button
            type="button"
            onClick={clearImage}
            className="text-sm text-stone-500 hover:text-stone-800 dark:text-stone-400 dark:hover:text-stone-100"
          >
            Clear
          </button>
        )}
      </div>
    </div>
  );
}
