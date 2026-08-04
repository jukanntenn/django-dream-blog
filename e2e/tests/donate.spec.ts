import { test, expect } from '@playwright/test';

test.describe('Donate', () => {
  test('donate page loads', async ({ page }) => {
    await page.goto('/donate/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('donate page shows content', async ({ page }) => {
    await page.goto('/donate/');
    // Donate page should have some content
    const content = page.locator('body');
    await expect(content).not.toBeEmpty();
  });
});
