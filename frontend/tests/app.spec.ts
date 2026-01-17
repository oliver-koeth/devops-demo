import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.clear();
  });
});

test('can create an incident and view it in list and detail', async ({ page }) => {
  await page.goto('/incidents');

  await page.getByTestId('incident-create-title').fill('API timeout alert');
  await page.getByTestId('incident-create-service').fill('Gateway');
  await page.getByTestId('incident-create-severity').selectOption('P2');
  await page.getByTestId('incident-create-submit').click();

  await expect(page.getByTestId('incident-detail-title')).toHaveText('API timeout alert');
  await page.getByTestId('incident-back').click();

  await expect(page.getByTestId('incident-list')).toContainText('API timeout alert');
});

test('incident persists after reload', async ({ page }) => {
  await page.goto('/incidents');

  await page.getByTestId('incident-create-title').fill('Cache miss spike');
  await page.getByTestId('incident-create-service').fill('Edge Cache');
  await page.getByTestId('incident-create-submit').click();

  await expect(page.getByTestId('incident-detail-title')).toHaveText('Cache miss spike');
  await page.reload();
  await page.getByTestId('incident-back').click();

  await expect(page.getByTestId('incident-list')).toContainText('Cache miss spike');
});

test('can create a runbook and see it after reload', async ({ page }) => {
  await page.goto('/runbooks');

  await page.getByTestId('runbook-create-title').fill('Service degradation response');
  await page.getByTestId('runbook-create-tags').fill('incident, response');
  await page.getByTestId('runbook-create-content').fill('Step 1: Acknowledge alert');
  await page.getByTestId('runbook-create-submit').click();

  await expect(page.getByTestId('runbook-detail-title')).toHaveText('Service degradation response');

  await page.reload();
  await expect(page.getByTestId('runbook-detail-title')).toHaveText('Service degradation response');
  await page.getByTestId('runbook-back').click();

  await expect(page.getByTestId('runbook-list')).toContainText('Service degradation response');
});
