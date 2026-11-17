import { test, expect } from '@playwright/test';

test('presentation login, refresh, all panels and chat', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.url().startsWith('http://127.0.0.1:5173') && response.status() >= 400)
      errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto('/login', { waitUntil: 'domcontentloaded' });
  await page.getByPlaceholder('Enter your username').fill('demo_farmer');
  await page.getByPlaceholder('Enter your password').fill('DemoFarmer@2026');
  await page.getByRole('button', { name: /Sign In/ }).click();
  await page.waitForURL('**/dashboard');
  await expect(page.getByLabel('Active field')).toHaveValue(/\d+/);
  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.getByLabel('Active field')).toHaveValue(/\d+/);
  for (const tab of ['home','my-field','field-report','data-analytics','field-log','pest','irrigation','yield-prediction','alerts','season-calendar','rotation','inventory','labor','equipment','cost-calculator','pnl-dashboard','market','forecast','schemes','insurance']) {
    await page.goto(`/dashboard#${tab}`, { waitUntil: 'domcontentloaded' });
    // Allow async panel requests and chart rendering to settle.
    await page.waitForTimeout(1000);
    await expect(page.getByText('Something went wrong', { exact: true })).toHaveCount(0);
  }
  await page.getByRole('button', { name: 'Open Chat' }).click();
  await page.getByPlaceholder('Ask a farming question…').fill('How should I irrigate?');
  await page.getByPlaceholder('Ask a farming question…').press('Enter');
  await expect(page.getByText(/Presentation demo — preset guidance/)).toBeVisible();
  expect(errors).toEqual([]);
});
