import { test, expect } from '@playwright/test';

test.describe('Favorites', () => {
  test('issues list page loads', async ({ page }) => {
    await page.goto('/favorites/issues/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('issues list shows seeded issue', async ({ page }) => {
    await page.goto('/favorites/issues/');
    // Should show the seeded issue
    await expect(page.locator('body')).toContainText('Issue #1');
  });

  test('issue detail page loads', async ({ page }) => {
    await page.goto('/favorites/issues/');
    // Find the issue link by its text content
    const issueLink = page.locator('a:has-text("Issue #1")').first();
    await expect(issueLink).toBeVisible({ timeout: 10_000 });
    await issueLink.click();

    // Should be on an issue detail page
    await expect(page).toHaveURL(/\/favorites\/issues\/\d+\//);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('issue detail shows favorites', async ({ page }) => {
    await page.goto('/favorites/issues/1/');
    // Should show favorites from the seeded data
    await expect(page.locator('body')).toContainText('Interesting Python Tool');
  });
});
