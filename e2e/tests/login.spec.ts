import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('NyayaSetu Login Journey', () => {
  test('should display login page and pass accessibility checks', async ({ page }) => {
    await page.goto('/login');
    
    // Accessibility check using axe-core
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    expect(accessibilityScanResults.violations).toEqual([]);

    // Functional check
    await expect(page.locator('h1')).toContainText('Login');
    await expect(page.locator('input[type="text"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // Fill credentials (assuming test user exists via DB seeding)
    await page.locator('input[placeholder="Username"]').fill('test_citizen');
    await page.locator('input[placeholder="Password"]').fill('testpass123');
    await page.locator('button[type="submit"]').click();

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=My Complaints')).toBeVisible();
  });
});
