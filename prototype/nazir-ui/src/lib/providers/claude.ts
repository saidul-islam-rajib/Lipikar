import Anthropic from "@anthropic-ai/sdk";
import type { VisionProvider, TranscriptionResult } from "./types";
import { TRANSCRIPTION_PROMPT } from "./types";
import { getEffectiveModel } from "@/lib/modelOverrides";

function client(): Anthropic {
  return new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
}

export const claudeProvider: VisionProvider = {
  id: "claude",
  label: "Claude (Anthropic)",

  isConfigured() {
    return Boolean(process.env.ANTHROPIC_API_KEY);
  },

  async transcribe(imageBase64, mimeType): Promise<TranscriptionResult> {
    const modelId = getEffectiveModel("claude");

    const response = await client().messages.create({
      model: modelId,
      max_tokens: 2048,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: mimeType as "image/jpeg" | "image/png" | "image/gif" | "image/webp",
                data: imageBase64,
              },
            },
            { type: "text", text: TRANSCRIPTION_PROMPT },
          ],
        },
      ],
    });

    const text = response.content
      .filter((block): block is Anthropic.TextBlock => block.type === "text")
      .map((block) => block.text)
      .join("\n")
      .trim();

    return { text, providerId: "claude", modelId };
  },
};
