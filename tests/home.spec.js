const { test, expect } = require("@playwright/test");

test.describe("DeepSeek V4 benchmark site", () => {
  test("desktop homepage renders SEO, core sections, and citations", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle("DeepSeek V4 Benchmark vs GPT-5.4, Claude, Gemini");
    await expect(page.locator("h1")).toHaveText("DeepSeek V4 Benchmark");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /DeepSeek V4 benchmark snapshot comparing GPT-5\.4/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://deepseekv4benchmark.lol/");
    await expect(page.locator('link[rel="icon"]').first()).toHaveAttribute("href", /favicon\.(svg|png)$/);
    await expect(page.locator('meta[property="og:locale"]')).toHaveAttribute("content", "en_US");
    await expect(page.locator('meta[name="twitter:image:alt"]')).toHaveAttribute(
      "content",
      "DeepSeek V4 Benchmark public comparison card"
    );

    await expect(page.getByRole("link", { name: "View comparison" })).toBeVisible();
    await expect(page.locator("#snapshot .snapshot-card")).toHaveCount(4);
    await expect(page.locator("#comparison .comparison-table")).toBeVisible();
    await expect(page.locator(".source-chip")).toHaveCount(8);
    await expect(page.locator("[data-source-count]")).toHaveText("8");
    await expect(page.locator("text=Not publicly disclosed").first()).toBeVisible();

    const comparisonText = page.locator("#comparison");
    await expect(comparisonText).toContainText("deepseek-v4-pro");
    await expect(comparisonText).toContainText("GPT-5.4");
    await expect(comparisonText).toContainText("Claude Opus 4.6");
    await expect(comparisonText).toContainText("Gemini 3.1 Pro");

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);

    const structuredData = await page.locator('script[type="application/ld+json"]').allTextContents();
    expect(structuredData.join("\n")).toContain('"@type": "WebSite"');
    expect(structuredData.join("\n")).toContain('"@type": "FAQPage"');

    await expect(page.locator('script[src*="googletagmanager"]')).toHaveCount(0);
    await expect(page.locator('script[src*="clarity"]')).toHaveCount(0);
  });

  test("mobile layout stays inside viewport and anchor navigation works", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await page.getByRole("link", { name: "View comparison" }).click();
    await expect(page.locator("#comparison")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await expect(page.locator("#faq details")).toHaveCount(5);
    await expect(page.locator(".source-card")).toHaveCount(8);

    await context.close();
  });

  test("health, robots, and sitemap endpoints stay publishable", async ({ request }) => {
    const health = await request.get("/healthz");
    expect(health.ok()).toBe(true);
    await expect.soft(await health.json()).toEqual({ ok: true });

    const robots = await request.get("/robots.txt");
    expect(robots.ok()).toBe(true);
    await expect.soft(await robots.text()).toContain("Sitemap: https://deepseekv4benchmark.lol/sitemap.xml");

    const sitemap = await request.get("/sitemap.xml");
    expect(sitemap.ok()).toBe(true);
    const sitemapText = await sitemap.text();
    expect(sitemapText).toContain("<loc>https://deepseekv4benchmark.lol/</loc>");
    expect(sitemapText).toContain("<lastmod>2026-04-24</lastmod>");
  });
});
