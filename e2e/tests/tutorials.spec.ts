import { test, expect } from '@playwright/test';

test.describe('Tutorials', () => {
  test('tutorial detail page loads', async ({ page }) => {
    await page.goto('/tutorials/getting-started-python/');
    await expect(page.locator('body')).not.toBeEmpty();
    await expect(page.locator('body')).toContainText('Getting Started with Python');
  });

  test('tutorial shows materials list', async ({ page }) => {
    await page.goto('/tutorials/getting-started-python/');
    // Should show materials for this tutorial
    await expect(page.locator('body')).toContainText('Installing Python');
    await expect(page.locator('body')).toContainText('Your First Script');
  });

  test('material detail page loads', async ({ page }) => {
    await page.goto('/tutorials/getting-started-python/');
    // Find a material link
    const materialLink = page.locator('a[href*="/materials/"]').first();
    await expect(materialLink).toBeVisible();
    await materialLink.click();

    // Should be on a material detail page
    await expect(page).toHaveURL(/\/tutorials\/.+\/materials\/\d+\//);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('material detail shows content', async ({ page }) => {
    await page.goto('/tutorials/getting-started-python/');
    const materialLink = page.locator('a[href*="/materials/"]').first();
    await expect(materialLink).toBeVisible();
    await materialLink.click();

    // Material should have visible content
    const content = page.locator('#content, .prose, article, main');
    await expect(content.first()).toBeVisible();
  });

  test('second tutorial page loads', async ({ page }) => {
    await page.goto('/tutorials/django-tutorial/');
    await expect(page.locator('body')).not.toBeEmpty();
    await expect(page.locator('body')).toContainText('Django Tutorial');
  });
});
