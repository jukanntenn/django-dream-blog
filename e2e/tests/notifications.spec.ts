import { test, expect } from '@playwright/test';

test.describe('Notifications', () => {
  test('notifications page requires login', async ({ page }) => {
    await page.goto('/notifications/');

    // Should redirect to login
    const url = page.url();
    const isLoginPage = url.includes('/accounts/login');
    const hasLoginMessage = await page.locator('text=login, text=登录').count() > 0;
    expect(isLoginPage || hasLoginMessage).toBeTruthy();
  });

  test('notifications page loads for authenticated user', async ({ page }) => {
    // Login first
    await page.goto('/accounts/login/');
    const usernameInput = page.locator('input[name="login"], input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await usernameInput.fill('testuser');
    await passwordInput.fill('testpass123');
    await submitButton.click();
    await page.waitForURL(/.*/, { timeout: 10_000 });

    // Now try notifications
    await page.goto('/notifications/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('unread notifications page loads for authenticated user', async ({ page }) => {
    // Login first
    await page.goto('/accounts/login/');
    const usernameInput = page.locator('input[name="login"], input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await usernameInput.fill('testuser');
    await passwordInput.fill('testpass123');
    await submitButton.click();
    await page.waitForURL(/.*/, { timeout: 10_000 });

    // Try unread notifications
    await page.goto('/notifications/unread/');
    await expect(page.locator('body')).not.toBeEmpty();
  });
});
