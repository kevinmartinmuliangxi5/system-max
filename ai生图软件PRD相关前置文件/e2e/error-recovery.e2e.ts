/// <reference types="detox" />
/// <reference types="jest" />

describe('Error Recovery E2E', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true, delete: true });
  });

  it('shows missing key guard before request', async () => {
    await expect(element(by.text('A-Chat Home'))).toBeVisible();
    await element(by.id('prompt-input')).typeText('test prompt');
    await element(by.id('send-btn')).tap();
    await expect(
      element(by.text('Missing API key. Save your key first.'))
    ).toBeVisible();
  });
});
