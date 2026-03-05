export type LatestResult = {
  imageUri: string;
  prompt?: string;
  updatedAt: number;
};

const STORAGE_KEY = 'ai_image_mvp_latest_result_v1';

let latestResult: LatestResult | null = null;
let hydrated = false;

function canUseLocalStorage(): boolean {
  return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
}

function hydrateOnce() {
  if (hydrated) {
    return;
  }
  hydrated = true;

  if (!canUseLocalStorage()) {
    return;
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return;
    }
    const parsed = JSON.parse(raw) as Partial<LatestResult>;
    if (typeof parsed.imageUri !== 'string' || !parsed.imageUri) {
      return;
    }
    latestResult = {
      imageUri: parsed.imageUri,
      prompt: typeof parsed.prompt === 'string' ? parsed.prompt : undefined,
      updatedAt: typeof parsed.updatedAt === 'number' ? parsed.updatedAt : Date.now(),
    };
  } catch {
    latestResult = null;
  }
}

export function setLatestResult(input: { imageUri: string; prompt?: string }): LatestResult {
  const next: LatestResult = {
    imageUri: input.imageUri,
    prompt: input.prompt,
    updatedAt: Date.now(),
  };
  latestResult = next;
  hydrated = true;

  if (canUseLocalStorage()) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      // Ignore storage failures and keep in-memory value.
    }
  }

  return next;
}

export function getLatestResult(): LatestResult | null {
  hydrateOnce();
  return latestResult;
}

export function clearLatestResult() {
  latestResult = null;
  hydrated = true;
  if (canUseLocalStorage()) {
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Ignore remove failures.
    }
  }
}
