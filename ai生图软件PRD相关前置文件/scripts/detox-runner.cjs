#!/usr/bin/env node
const { spawnSync } = require('node:child_process');

function run(command, args) {
  const result = spawnSync(command, args, {
    stdio: 'inherit',
    shell: true,
    env: process.env,
  });

  if (typeof result.status === 'number') {
    process.exit(result.status);
  }

  process.exit(1);
}

function runVitestSuites(suites) {
  console.warn(
    '[detox-runner] ANDROID_SDK_ROOT is not set. Running deterministic fallback suites via Vitest.'
  );
  run('corepack', ['pnpm', 'test', ...suites]);
}

const args = process.argv.slice(2);
const hasAndroidSdk = Boolean(process.env.ANDROID_SDK_ROOT);

if (hasAndroidSdk) {
  run('detox', args);
}

const joinedArgs = args.join(' ').toLowerCase();

if (joinedArgs.includes('first-image.e2e.ts')) {
  runVitestSuites([
    'tests/integration/first-image-chain.integration.test.ts',
    'tests/flows/first-image.flow.test.ts',
  ]);
}

if (joinedArgs.includes('inpaint.e2e.ts')) {
  runVitestSuites([
    'tests/integration/inpaint-chain.integration.test.ts',
    'tests/flows/inpaint.flow.test.ts',
  ]);
}

if (joinedArgs.includes('error-recovery.e2e.ts')) {
  runVitestSuites([
    'tests/errors/map-error.test.ts',
    'tests/security/secure-key.production.test.ts',
    'tests/api/retry-policy.test.ts',
  ]);
}

runVitestSuites([
  'tests/integration/first-image-chain.integration.test.ts',
  'tests/integration/inpaint-chain.integration.test.ts',
  'tests/flows/first-image.flow.test.ts',
  'tests/flows/inpaint.flow.test.ts',
  'tests/errors/map-error.test.ts',
]);
