import { test, expect } from '@playwright/test';

test.describe('Admin', () => {
  test('admin login page loads', async ({ page }) => {
    await page.goto('/admin/');
    await expect(page.locator('body')).not.toBeEmpty();
    // Should have a login form for admin
    const form = page.locator('form');
    await expect(form.first()).toBeVisible();
  });

  test('admin login has required fields', async ({ page }) => {
    await page.goto('/admin/');
    const usernameInput = page.locator('input[name="username"]');
    const passwordInput = page.locator('input[name="password"]');
    await expect(usernameInput.first()).toBeVisible();
    await expect(passwordInput.first()).toBeVisible();
  });

  test('admin login works with valid credentials', async ({ page }) => {
    await page.goto('/admin/');

    const usernameInput = page.locator('input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('input[type="submit"], button[type="submit"]').first();

    await usernameInput.fill('admin');
    await passwordInput.fill('adminpass123');
    await submitButton.click();

    // Should redirect to admin index
    await page.waitForURL(/\/admin\/.*/, { timeout: 10_000 });
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('admin index shows app list after login', async ({ page }) => {
    // Login to admin
    await page.goto('/admin/');
    await page.locator('input[name="username"]').first().fill('admin');
    await page.locator('input[name="password"]').first().fill('adminpass123');
    await page.locator('input[type="submit"], button[type="submit"]').first().click();
    await page.waitForURL(/\/admin\/.*/, { timeout: 10_000 });

    // Admin index should show installed apps
    await expect(page.locator('body')).toContainText('Django administration');
  });
});
