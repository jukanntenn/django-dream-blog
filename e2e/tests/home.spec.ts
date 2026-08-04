import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('loads and displays content', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/.*/);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('displays navigation links', async ({ page }) => {
    await page.goto('/');
    const nav = page.locator('#site-nav, nav, header');
    await expect(nav.first()).toBeVisible({ timeout: 10_000 });
  });

  test('shows published posts on home page', async ({ page }) => {
    await page.goto('/');
    // Home page should display published posts
    await expect(page.locator('body')).toContainText('First Blog Post');
    await expect(page.locator('body')).toContainText('Second Blog Post');
  });

  test('does not show draft posts', async ({ page }) => {
    await page.goto('/');
    // Draft posts should not appear on the home page
    await expect(page.locator('body')).not.toContainText('Draft Post');
  });

  test('post links navigate to detail page', async ({ page }) => {
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();
    await expect(page).toHaveURL(/\/posts\/\d+\//);
  });
});
