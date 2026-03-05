# AI Image MVP

## Acceptance Commands

```bash
pnpm test
pnpm typecheck
pnpm lint
pnpm build
```

## Detox E2E

```bash
pnpm detox test e2e/first-image.e2e.ts --configuration android.emu.debug
pnpm detox test e2e/inpaint.e2e.ts --configuration android.emu.debug
pnpm detox test e2e/error-recovery.e2e.ts --configuration android.emu.debug
```

Environment prerequisites:
- `ANDROID_SDK_ROOT` must point to a valid Android SDK.
- Android emulator `Pixel_7_API_34` should be available or update `.detoxrc.js`.

When `ANDROID_SDK_ROOT` is not set, `pnpm detox ...` runs deterministic Vitest fallback suites for the same critical paths.
