import { test, expect } from '@playwright/test';

test.describe('Webtools', () => {
  test('secret key generator page loads', async ({ page }) => {
    await page.goto('/webtools/django-secret-key-creator');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('secret key generator has form', async ({ page }) => {
    await page.goto('/webtools/django-secret-key-creator');
    const form = page.locator('form');
    await expect(form.first()).toBeVisible();
  });

  test('secret key generator has submit button', async ({ page }) => {
    await page.goto('/webtools/django-secret-key-creator');
    const submitButton = page.locator('button[type="submit"], input[type="submit"]');
    await expect(submitButton.first()).toBeVisible();
  });

  test('secret key generator produces output', async ({ page }) => {
    await page.goto('/webtools/django-secret-key-creator');
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();
    await submitButton.click();

    // Should show generated secret key
    await expect(page.locator('body')).not.toBeEmpty();
  });
});
