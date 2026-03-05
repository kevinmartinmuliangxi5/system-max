/// <reference types="detox" />
/// <reference types="jest" />

describe('First Image E2E', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('generates first image and shows result card', async () => {
    await expect(element(by.text('A-Chat Home'))).toBeVisible();
    await element(by.id('api-key-input')).typeText('sk-e2e-demo');
    await element(by.id('save-api-key-btn')).tap();
    await element(by.id('prompt-input')).typeText('a city skyline');
    await element(by.id('send-btn')).tap();
    await expect(element(by.text('Result Card'))).toBeVisible();
  });
});
