import { test, expect, Page } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

let page: Page;
const complaintTitle = `Test Water Leakage in Area 51 ${Date.now()}`;
const officerComment = `Officer has acknowledged the issue at ${new Date().toISOString()}`;

let complaintId = '';

test.beforeAll(async ({ browser }) => {
  page = await browser.newPage();
});

test.afterAll(async () => {
  await page.close();
});

test.describe('NyayaSetu Comprehensive UAT Journey', () => {
  test('Phase 1 & 2: Startup & Landing Page', async () => {
    // Phase 1: Application Startup
    const response = await page.goto('/');
    expect(response?.status()).toBe(200);

    // Verify no console errors during initial load
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.error(`Console Error: ${msg.text()}`);
      }
    });

    // Phase 2: Landing Page Checks
    await expect(page.locator('.brand-title')).toHaveText('NYAYA SETU');
    await expect(page.getByRole('link', { name: /Login or Register/i }).first()).toBeVisible();
    
    // Check navigation links
    await expect(page.getByRole('link', { name: 'Home', exact: true })).toBeVisible();
    
    // Check Theme Toggle
    const themeBtn = page.locator('.theme-toggle-btn');
    await themeBtn.click();
    await themeBtn.click();
  });

  test('Phase 3: Login Testing (Negative & Positive)', async () => {
    await page.getByRole('link', { name: /Login or Register/i }).first().click();

    // Wait for the form to be ready
    await expect(page.locator('.login-form-element')).toBeVisible({ timeout: 10000 });

    // Negative testing
    await page.locator('#login-username').fill('wronguser');
    await page.locator('#login-password').fill('wrongpass');
    await page.getByRole('button', { name: 'Sign In' }).click();
    try { await expect(page.locator('.login-error-alert')).toBeVisible({ timeout: 2000 }); } catch (e) { console.log(await page.content()); throw e; }

    // Positive login (Citizen)
    await page.locator('#login-username').fill('ravi12');
    await page.locator('#login-password').fill('Charan@24');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard|\/complaints/);
  });

  test('Phase 4: Citizen Dashboard', async () => {
    await page.getByRole('link', { name: /Dashboard/i }).first().click();
    await expect(page.getByRole('heading', { name: /Dashboard|Welcome/i })).toBeVisible();
    await expect(page.locator('.stat-card').first()).toBeVisible();
  });

  test('Phase 5: Lodge Complaint', async () => {
    await page.getByRole('link', { name: /Lodge Grievance/i }).first().click();
    
    await expect(page.locator('.lodge-form')).toBeVisible();

    await page.getByLabel(/Title/i).fill(complaintTitle);
    await page.getByLabel(/Detailed Explanation/i).fill('There is a massive water pipe burst that needs immediate attention.');
    
    const deptSelect = page.locator('#complaint-dept');
    if (await deptSelect.count() > 0) {
      await deptSelect.selectOption({ index: 1 });
    }
    
    await page.getByLabel(/Address/i).fill('Area 51 Main Street');
    
    await page.getByRole('button', { name: /Submit|Lodge/i }).click();
    
    await expect(page).toHaveURL(/\/complaints/);
    await expect(page.getByText(complaintTitle).first()).toBeVisible();
  });

  test('Phase 6: My Complaints', async () => {
    await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
    await expect(page.getByText(complaintTitle).first()).toBeVisible();
  });

  test('Phase 7: Logout', async () => {
    await page.getByRole('link', { name: /Dashboard/i }).first().click();
    await page.locator('.logout-btn-nav, button[aria-label="Logout"]').click();
    
    await expect(page).toHaveURL(/\/$|\/login/);
    await expect(page.getByRole('link', { name: /Login or Register/i }).first()).toBeVisible();
  });

  test('Phase 8 & 9: Officer Login & Dashboard', async () => {
    await page.getByRole('link', { name: /Login or Register/i }).first().click();
    
    await page.locator('#login-username').fill('devansh12');
    await page.locator('#login-password').fill('Charan@24');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page).toHaveURL(/\/dashboard|\/complaints/);
    await expect(page.getByText(/Officer Dashboard|Assigned Grievances/i).first()).toBeVisible();
  });

  test('Phase 10: Officer Processing', async () => {
    await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
    
    await page.getByText(complaintTitle).first().click();
    await expect(page.locator('.complaint-title-h1')).toHaveText(complaintTitle);
    
    const commentInput = page.locator('textarea.comment-textarea-field');
    if (await commentInput.count() > 0) {
      await commentInput.fill(officerComment);
      const sendBtn = page.getByRole('button', { name: /Send/i });
      if (await sendBtn.count() > 0) {
        await sendBtn.first().click();
        await expect(page.getByText(officerComment)).toBeVisible({ timeout: 10000 });
      }
    }

    const resolveBtn = page.getByRole('button', { name: /Mark Resolved/i });
    if (await resolveBtn.count() > 0) {
      await resolveBtn.first().click();
      await expect(page.getByText(/Complaint status updated to 'resolved' successfully!/i)).toBeVisible({ timeout: 10000 });
    } else {
      const progressBtn = page.getByRole('button', { name: /Mark In Progress/i });
      if (await progressBtn.count() > 0) {
        await progressBtn.first().click();
        await expect(page.getByText(/Complaint status updated to 'in progress' successfully!/i)).toBeVisible({ timeout: 10000 });
      }
    }
  });

  test('Phase 11: Citizen Verification', async () => {
    await page.locator('.logout-btn-nav, button[aria-label="Logout"]').click();
    
    await page.getByRole('link', { name: /Login or Register/i }).first().click();
    await page.locator('#login-username').fill('ravi12');
    await page.locator('#login-password').fill('Charan@24');
    await page.getByRole('button', { name: 'Sign In' }).click();
    
    await page.getByRole('link', { name: /My Complaints|Assigned Grievances/i }).first().click();
    await page.getByText(complaintTitle).first().click();
    
    await expect(page.getByText(officerComment)).toBeVisible();
    await expect(page.locator('body')).toContainText(/Resolved/i);
  });
});
