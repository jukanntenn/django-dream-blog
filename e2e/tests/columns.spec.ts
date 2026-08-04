import { test, expect } from '@playwright/test';

test.describe('Columns', () => {
  test('column detail page loads', async ({ page }) => {
    await page.goto('/columns/weekly-picks/');
    await expect(page.locator('body')).not.toBeEmpty();
    await expect(page.locator('body')).toContainText('Weekly Picks');
  });

  test('column shows articles list', async ({ page }) => {
    await page.goto('/columns/weekly-picks/');
    // Should show articles for this column
    await expect(page.locator('body')).toContainText('Pick #1');
    await expect(page.locator('body')).toContainText('Pick #2');
  });

  test('article detail page loads', async ({ page }) => {
    await page.goto('/columns/weekly-picks/');
    // Find an article link
    const articleLink = page.locator('a[href*="/articles/"]').first();
    await expect(articleLink).toBeVisible();
    await articleLink.click();

    // Should be on an article detail page
    await expect(page).toHaveURL(/\/columns\/.+\/articles\/\d+\//);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('article detail shows content', async ({ page }) => {
    await page.goto('/columns/weekly-picks/');
    const articleLink = page.locator('a[href*="/articles/"]').first();
    await expect(articleLink).toBeVisible();
    await articleLink.click();

    // Article should have visible content
    const content = page.locator('#content, .prose, article, main');
    await expect(content.first()).toBeVisible();
  });

  test('article detail shows comment section', async ({ page }) => {
    await page.goto('/columns/weekly-picks/');
    const articleLink = page.locator('a[href*="/articles/"]').first();
    await expect(articleLink).toBeVisible();
    await articleLink.click();

    // Check for comment-related elements
    const comments = page.locator('.comments, .comment-section, #comments, [class*="comment"], form[action*="comment"]');
    await expect(comments.first()).toBeVisible();
  });
});
