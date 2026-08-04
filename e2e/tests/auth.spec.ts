import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('login page loads', async ({ page }) => {
    await page.goto('/accounts/login/');
    await expect(page.locator('body')).not.toBeEmpty();
    // Should have a login form
    const form = page.locator('form');
    await expect(form.first()).toBeVisible();
  });

  test('login form has required fields', async ({ page }) => {
    await page.goto('/accounts/login/');
    // Should have username/email and password inputs
    const usernameInput = page.locator('input[name="login"], input[name="username"]');
    const passwordInput = page.locator('input[name="password"]');
    await expect(usernameInput.first()).toBeVisible();
    await expect(passwordInput.first()).toBeVisible();
  });

  test('login form accepts valid credentials', async ({ page }) => {
    await page.goto('/accounts/login/');

    const usernameInput = page.locator('input[name="login"], input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await usernameInput.fill('testuser');
    await passwordInput.fill('testpass123');
    await submitButton.click();

    // Should redirect after login (not stay on login page)
    await page.waitForURL(/.*/, { timeout: 10_000 });
    const url = page.url();
    expect(url).not.toContain('/accounts/login');
  });

  test('protected pages redirect to login', async ({ page }) => {
    // Try to access notifications without login
    await page.goto('/notifications/');

    // Should redirect to login
    const url = page.url();
    const isLoginPage = url.includes('/accounts/login');
    const hasLoginMessage = await page.locator('text=login, text=登录').count() > 0;
    expect(isLoginPage || hasLoginMessage).toBeTruthy();
  });

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.goto('/accounts/login/');

    const usernameInput = page.locator('input[name="login"], input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await usernameInput.fill('invaliduser');
    await passwordInput.fill('wrongpassword');
    await submitButton.click();

    // Should stay on login page or show error
    await page.waitForURL(/.*/, { timeout: 10_000 });
    const url = page.url();
    const hasError = await page.locator('.error, .alert, .message, [class*="error"]').count() > 0;
    // Either stayed on login or showed error message
    expect(url.includes('/accounts/login') || hasError).toBeTruthy();
  });
});
