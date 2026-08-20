# nazir-ui prototype

A throwaway demo: upload a photo of a handwritten deed (দলিল) and get a best-effort draft
transcription back from a general-purpose vision AI model (Claude, GPT-4o, or Gemini — your
choice).

**This is not the real `nazir` pipeline stage.** It skips the whole Lipikar BMAD process (no
story, no QA gate, no Architect review) and calls a general AI model instead of a model trained on
Bengali deed handwriting. It exists so there is something to actually try today, while the real
epic-by-epic pipeline (`docs/epics/`, `docs/prd.md` in the repo root) gets built properly. Treat
every result as a rough draft a human must verify against the original — never as authoritative.

## Stack

- **Next.js 16** (App Router, TypeScript)
- **Tailwind CSS v4**
- **Jotai** for client state — chosen over Redux for a small app: a handful of independent atoms
  (selected provider, uploaded image, result, request status) with none of Redux's
  store/reducer/action boilerplate.
- Hand-rolled admin session (HMAC-signed cookie, `src/lib/session.ts`) instead of a library like
  NextAuth, since this stack (Next 16 + React 19) is new enough that a large auth library's peer
  dependencies were a real risk. Fine for a local prototype; not hardened for production (no rate
  limiting, no lockout, single shared credential).
- No database. Nothing is persisted — uploaded images and transcriptions live only in the
  browser and in the API request/response; the server never writes them to disk. The admin
  dashboard only shows in-memory counts (requests per provider), which reset on restart.

## Setup

```bash
cd prototype/nazir-ui
npm install          # already done if you're continuing from initial setup
cp env.template.txt .env.local
```

Edit `.env.local`:
- Set at least one provider's API key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GEMINI_API_KEY`).
  Only providers with a key show up as selectable in the UI.
- Set `SESSION_SECRET` to a random value: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`
- Set `ADMIN_USERNAME` / `ADMIN_PASSWORD` to whatever you want for the `/admin` login.

## Run

```bash
npm run dev
```

Open http://localhost:3000 — no login needed to upload and transcribe a photo.
Open http://localhost:3000/admin to sign in and see which providers are configured and basic
request counts.

## Notes

- Max upload size is 8MB, validated both client- and server-side.
- The transcription prompt (`src/lib/providers/types.ts`) explicitly tells the model to mark
  illegible text as `[অস্পষ্ট]` rather than guess, and to transcribe rather than translate —
  mirroring the real pipeline's assistive-only stance even though this prototype isn't bound by
  its rules.
- Model IDs are set via env vars with defaults in `env.template.txt` — update them there if a
  provider ships a newer model by the time you're using this.
