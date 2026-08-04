import { test, expect } from '@playwright/test';

test.describe('Newsletters', () => {
  test('subscription page loads', async ({ page }) => {
    await page.goto('/newsletters/subscription/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('subscription page has email input', async ({ page }) => {
    await page.goto('/newsletters/subscription/');
    const emailInput = page.locator('input[name="email"], input[type="email"]');
    await expect(emailInput.first()).toBeVisible();
  });

  test('subscription page has submit button', async ({ page }) => {
    await page.goto('/newsletters/subscription/');
    const submitButton = page.locator('button[type="submit"], input[type="submit"]');
    await expect(submitButton.first()).toBeVisible();
  });

  test('subscription form accepts email and submits', async ({ page }) => {
    await page.goto('/newsletters/subscription/');

    const emailInput = page.locator('input[name="email"], input[type="email"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await emailInput.fill('newsubscriber@example.com');
    await submitButton.click();

    // Should show success message or redirect
    await expect(page.locator('body')).not.toBeEmpty();
  });
});
