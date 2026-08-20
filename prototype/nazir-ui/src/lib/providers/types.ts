export type ProviderId = "claude" | "openai" | "gemini";

export interface ProviderInfo {
  id: ProviderId;
  label: string;
  configured: boolean;
}

export interface TranscriptionResult {
  text: string;
  providerId: ProviderId;
  modelId: string;
}

export interface VisionProvider {
  id: ProviderId;
  label: string;
  isConfigured(): boolean;
  transcribe(imageBase64: string, mimeType: string): Promise<TranscriptionResult>;
}

export const TRANSCRIPTION_PROMPT = `You are assisting with transcribing a photograph of a handwritten Bangladeshi land deed (দলিল). The document may mix handwritten Bengali (Bangla script) and English, and may use archaic Bengali revenue vocabulary (e.g. মৌজা, খতিয়ান, দাগ).

Transcribe the visible text as accurately as possible:
- Preserve the original language of each part; do not translate.
- Preserve line breaks where they are discernible.
- If a word or phrase is illegible or you are not confident, write [অস্পষ্ট] in its place instead of guessing.
- Do not add commentary, headings, or explanation — output only the transcription.

This is a best-effort draft for a human to verify against the original document, not a final or authoritative reading.`;
