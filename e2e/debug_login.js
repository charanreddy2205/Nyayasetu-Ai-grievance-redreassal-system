const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8000/login');

  console.log('page title:', await page.title());
  await page.locator('#login-username').fill('wronguser');
  await page.locator('#login-password').fill('wrongpass');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await page.waitForTimeout(2500);
  const invalidCount = await page.locator('.login-error-alert').count();
  console.log('invalid count', invalidCount);
  console.log('invalid visible', invalidCount > 0 ? await page.locator('.login-error-alert').isVisible() : false);
  console.log('url after invalid', page.url());
  console.log('body text contains error:', (await page.locator('body').textContent()).includes('Invalid username or password.') );

  await page.locator('#login-username').fill('ravi12');
  await page.locator('#login-password').fill('Charan@24');
  await page.getByRole('button', { name: 'Sign In' }).click();
  try {
    await page.waitForURL(/\/dashboard|\/complaints/, { timeout: 8000 });
  } catch (e) {
    console.log('did not redirect:', e.message);
  }
  console.log('final url', page.url());
  console.log('final body snippet', (await page.locator('body').textContent()).slice(0, 500));
  await browser.close();
})();
