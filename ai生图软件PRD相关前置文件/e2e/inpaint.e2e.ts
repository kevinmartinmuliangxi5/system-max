/// <reference types="detox" />
/// <reference types="jest" />

describe('Inpaint E2E', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('applies inpaint action from editor screen', async () => {
    await element(by.text('Go to Editor')).tap();
    await expect(element(by.text('A-Editor'))).toBeVisible();
    await element(by.id('source-image-uri-input')).replaceText('file://origin.png');
    await element(by.id('mask-uri-input')).replaceText('file://mask.png');
    await element(by.id('inpaint-instruction-input')).replaceText('replace sky');
    await element(by.id('apply-inpaint-btn')).tap();
    await expect(element(by.id('updated-uri-text'))).toBeVisible();
  });
});
