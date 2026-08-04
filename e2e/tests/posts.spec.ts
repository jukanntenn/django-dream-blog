import { test, expect } from '@playwright/test';

test.describe('Posts', () => {
  test('post detail page loads with content', async ({ page }) => {
    // Navigate via home page to find a post link
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();

    // Should be on a post detail page
    await expect(page).toHaveURL(/\/posts\/\d+\//);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('post detail shows title', async ({ page }) => {
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();

    // The post title should be visible on the detail page
    const heading = page.locator('h1, h2, .post-title, .entry-title').first();
    await expect(heading).toBeVisible();
  });

  test('post detail shows comment section', async ({ page }) => {
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    await expect(postLink).toBeVisible();
    await postLink.click();

    // Check for comment-related elements
    const comments = page.locator('.comments, .comment-section, #comments, [class*="comment"], form[action*="comment"]');
    await expect(comments.first()).toBeVisible();
  });

  test('archives page loads', async ({ page }) => {
    await page.goto('/archives/');
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('archives page shows posts', async ({ page }) => {
    await page.goto('/archives/');
    // Archives should list published posts
    await expect(page.locator('body')).toContainText('First Blog Post');
  });

  test('direct post URL loads correctly', async ({ page }) => {
    // Navigate to home first to discover a post URL
    await page.goto('/');
    const postLink = page.locator('a[href*="/posts/"]').first();
    const href = await postLink.getAttribute('href');
    expect(href).toBeTruthy();

    // Navigate directly to the post URL
    await page.goto(href!);
    await expect(page).toHaveURL(/\/posts\/\d+\//);
    await expect(page.locator('body')).not.toBeEmpty();
  });
});
