import { GoogleGenerativeAI } from "@google/generative-ai";
import type { VisionProvider, TranscriptionResult } from "./types";
import { TRANSCRIPTION_PROMPT } from "./types";

const DEFAULT_MODEL = "gemini-2.0-flash";

function client(): GoogleGenerativeAI {
  return new GoogleGenerativeAI(process.env.GEMINI_API_KEY ?? "");
}

export const geminiProvider: VisionProvider = {
  id: "gemini",
  label: "Gemini (Google)",

  isConfigured() {
    return Boolean(process.env.GEMINI_API_KEY);
  },

  async transcribe(imageBase64, mimeType): Promise<TranscriptionResult> {
    const modelId = process.env.GEMINI_MODEL || DEFAULT_MODEL;
    const model = client().getGenerativeModel({ model: modelId });

    const result = await model.generateContent([
      TRANSCRIPTION_PROMPT,
      { inlineData: { data: imageBase64, mimeType } },
    ]);

    const text = result.response.text().trim();

    return { text, providerId: "gemini", modelId };
  },
};
