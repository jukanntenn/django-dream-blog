import { test, expect } from '@playwright/test';

test.describe('Feeds and Sitemaps', () => {
  test('RSS feed loads', async ({ page }) => {
    const response = await page.goto('/rss.xml');
    expect(response?.status()).toBe(200);
    const contentType = response?.headers()['content-type'];
    expect(contentType).toContain('xml');
  });

  test('sitemap loads', async ({ page }) => {
    const response = await page.goto('/sitemap.xml');
    expect(response?.status()).toBe(200);
    const contentType = response?.headers()['content-type'];
    expect(contentType).toContain('xml');
  });

  test('sitemap contains URLs', async ({ page }) => {
    await page.goto('/sitemap.xml');
    const content = await page.locator('body').textContent();
    expect(content).toContain('<url>');
  });
});
