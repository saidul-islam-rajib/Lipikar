import OpenAI from "openai";
import type { VisionProvider, TranscriptionResult } from "./types";
import { TRANSCRIPTION_PROMPT } from "./types";
import { getEffectiveModel } from "@/lib/modelOverrides";

function client(): OpenAI {
  return new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
}

export const openaiProvider: VisionProvider = {
  id: "openai",
  label: "GPT-4o (OpenAI)",

  isConfigured() {
    return Boolean(process.env.OPENAI_API_KEY);
  },

  async transcribe(imageBase64, mimeType): Promise<TranscriptionResult> {
    const modelId = getEffectiveModel("openai");

    const response = await client().chat.completions.create({
      model: modelId,
      max_tokens: 2048,
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: TRANSCRIPTION_PROMPT },
            {
              type: "image_url",
              image_url: { url: `data:${mimeType};base64,${imageBase64}` },
            },
          ],
        },
      ],
    });

    const text = response.choices[0]?.message?.content?.trim() ?? "";

    return { text, providerId: "openai", modelId };
  },
};
