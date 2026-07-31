const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8000/login');

  const session = await page.evaluate(async () => {
    const r = await fetch('/api/auth/session/', { headers: { Accept: 'application/json' } });
    return await r.json();
  });
  console.log('session', JSON.stringify(session));

  const loginResp = await page.evaluate(async (csrfToken) => {
    const r = await fetch('/api/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ username: 'ravi12', password: 'Charan@24' }),
      credentials: 'include',
    });
    const text = await r.text();
    return { status: r.status, text };
  }, session.csrfToken);

  console.log('loginResp', JSON.stringify(loginResp));
  await browser.close();
})();
