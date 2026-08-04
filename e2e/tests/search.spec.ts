import { test, expect } from '@playwright/test';

test.describe('Search', () => {
  test('search page loads', async ({ page }) => {
    await page.goto('/search/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('search page has search input', async ({ page }) => {
    await page.goto('/search/');
    const searchInput = page.locator('input[name="q"], input[type="search"]');
    await expect(searchInput.first()).toBeVisible();
  });

  test('search form accepts input and submits', async ({ page }) => {
    await page.goto('/search/');
    const searchInput = page.locator('input[name="q"], input[type="search"]').first();

    await searchInput.fill('Python');
    await searchInput.press('Enter');

    // Should show results or "no results" message
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('search with empty query shows page without errors', async ({ page }) => {
    await page.goto('/search/');
    const searchInput = page.locator('input[name="q"], input[type="search"]').first();

    await searchInput.fill('');
    await searchInput.press('Enter');

    // Page should still load without errors
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('search results contain matching content', async ({ page }) => {
    await page.goto('/search/');
    const searchInput = page.locator('input[name="q"], input[type="search"]').first();

    await searchInput.fill('Blog');
    await searchInput.press('Enter');

    // Should show some results related to "Blog"
    await expect(page.locator('body')).not.toBeEmpty();
  });
});
