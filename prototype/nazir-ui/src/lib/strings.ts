export const strings = {
  app: {
    title: "Lipikar — deed transcription prototype",
    description: "Upload a photo of a handwritten deed and get a draft transcription.",
  },

  header: {
    appName: "Lipikar",
    tagline: "দলিল transcription prototype",
    adminLink: "Admin",
  },

  footer: {
    notice:
      "Prototype only. Images are sent to the AI provider you select for this request and are not stored by this app.",
  },

  assistiveNotice: {
    heading: "This is a prototype, not the trained Lipikar pipeline.",
    body: "Transcriptions come from a general-purpose AI model, not a model trained on Bengali deed handwriting. Treat every result as a rough draft that a human must verify against the original document — never rely on it for a legal purpose.",
  },

  home: {
    heading: "Upload a দলিল photo",
    subheading:
      "Get a best-effort draft transcription of handwritten Bengali and English text. No sign-in needed — nothing you upload is stored on this server.",
  },

  providerSelect: {
    label: "AI provider",
    loading: "Loading providers…",
    unconfiguredHint: "No API key configured on the server",
  },

  upload: {
    invalidType: "Please choose a JPEG, PNG, WebP, or GIF image.",
    tooLarge: "Image is larger than 8MB. Please choose a smaller photo.",
    dropPrompt: "Click to choose a photo, or drag one here",
    acceptedFormats: "JPEG, PNG, WebP, or GIF · up to 8MB",
    previewAlt: "Selected deed photo",
    transcribing: "Transcribing…",
    transcribe: "Transcribe",
    clear: "Clear",
    genericError: "Transcription failed.",
  },

  result: {
    genericError: "Something went wrong.",
    reading: "Reading the photo…",
    draftLabel: (modelId: string) => `Draft transcription · ${modelId}`,
    copy: "Copy text",
    copied: "Copied",
    empty: "No text was detected in this image.",
  },

  adminLogin: {
    heading: "Admin sign in",
    username: "Username",
    password: "Password",
    signingIn: "Signing in…",
    signIn: "Sign in",
    genericError: "Login failed.",
  },

  admin: {
    heading: "Admin",
    signOut: "Sign out",
    providerConfigHeading: "Provider configuration",
    keyConfigured: "Key configured",
    noKeySet: "No key set",
    keyHint:
      "Set API keys as environment variables on the server (see env.template.txt). No key value is ever shown here.",
    activeProviderHeading: "Active provider",
    activeProviderHint:
      "Only one provider is active at a time. The active provider is what the public upload page uses by default.",
    activeProviderGenericError: "Could not change the active provider.",
    sessionUsageHeading: "Session usage",
    sessionUsageHint:
      "Counts only, reset on server restart. No uploaded image or transcription text is ever stored.",
    uptime: "Uptime",
    requests: "Requests",
    failures: "Failures",
    byProvider: "By provider",
  },

  api: {
    invalidTranscribeRequest:
      "Invalid request. Expected providerId, mimeType, and imageBase64 (max 8MB).",
    providerNotConfigured: (label: string) =>
      `${label} is not configured on this server. Set its API key in .env.local.`,
    transcriptionFailed: "Transcription failed.",
    loginFieldsRequired: "Username and password are required.",
    adminLoginNotConfigured: "Admin login is not configured on this server.",
    invalidCredentials: "Invalid username or password.",
    notSignedIn: "Not signed in.",
    providerIdRequired: "providerId is required.",
    cannotActivateUnconfigured: (label: string) =>
      `${label} has no API key configured, so it cannot be made active.`,
  },
} as const;
