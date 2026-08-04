import { test, expect } from '@playwright/test';

test.describe('Comments', () => {
  test('comment form is visible on post detail page', async ({ page }) => {
    // Navigate to a post detail page
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();
    await expect(page).toHaveURL(/\/posts\/\d+\//);

    // Comment form or comment section should be visible
    const commentSection = page.locator('.comments, .comment-section, #comments, [class*="comment"]');
    await expect(commentSection.first()).toBeVisible();
  });

  test('comment form requires login', async ({ page }) => {
    // Navigate to a post detail page
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();

    // Try to post a comment without login
    const commentForm = page.locator('form[action*="comment"], .comment-form');
    if (await commentForm.count() > 0) {
      const textarea = commentForm.locator('textarea, input[name="comment"]');
      if (await textarea.count() > 0) {
        await textarea.first().fill('Test comment');
        const submitBtn = commentForm.locator('button[type="submit"], input[type="submit"]');
        if (await submitBtn.count() > 0) {
          await submitBtn.first().click();
          // Should redirect to login or show login required
          await page.waitForURL(/.*/, { timeout: 10_000 });
          const url = page.url();
          const hasLoginMessage = await page.locator('text=login, text=登录, text=Login').count() > 0;
          expect(url.includes('/accounts/login') || hasLoginMessage).toBeTruthy();
        }
      }
    }
  });

  test('authenticated user can see comment form', async ({ page }) => {
    // Login first
    await page.goto('/accounts/login/');
    const usernameInput = page.locator('input[name="login"], input[name="username"]').first();
    const passwordInput = page.locator('input[name="password"]').first();
    const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();

    await usernameInput.fill('testuser');
    await passwordInput.fill('testpass123');
    await submitButton.click();
    await page.waitForURL(/.*/, { timeout: 10_000 });

    // Navigate to a post
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();
    await expect(page).toHaveURL(/\/posts\/\d+\//);

    // Comment section should be visible for authenticated user
    const commentSection = page.locator('.comments, .comment-section, #comments, [class*="comment"]');
    await expect(commentSection.first()).toBeVisible();
  });
});
