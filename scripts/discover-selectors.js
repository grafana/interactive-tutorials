#!/usr/bin/env node

/**
 * Selector discovery script - bypasses MCP, runs Playwright directly
 * Usage: node scripts/discover-selectors.js <url>
 */

const { chromium } = require('playwright');

const path = require('path');
const userDataDir = path.join(__dirname, '.browser-session');

async function discoverSelectors(url) {
    console.log(`\n🔍 Discovering selectors for: ${url}\n`);

    // Use persistent context to keep login session
    const context = await chromium.launchPersistentContext(userDataDir, {
        headless: false,
        viewport: { width: 1400, height: 900 }
    });
    const page = context.pages()[0] || await context.newPage();

    try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        console.log('✅ Page loaded\n');

        // Wait for user to log in if needed
        console.log('👉 LOG IN NOW if you see a login page.');
        console.log('⏳ Waiting 60 seconds for you to log in...');
        console.log('   (Press Enter in this terminal when ready to capture selectors)\n');

        // Wait up to 60 seconds, or until user presses Enter
        await Promise.race([
            page.waitForTimeout(60000),
            new Promise(resolve => {
                process.stdin.once('data', resolve);
            })
        ]);

        // Get all interactive elements with useful attributes
        const selectors = await page.evaluate(() => {
            const elements = [];

            // Find elements with data-testid
            document.querySelectorAll('[data-testid]').forEach(el => {
                elements.push({
                    type: 'data-testid',
                    selector: `[data-testid="${el.getAttribute('data-testid')}"]`,
                    tag: el.tagName.toLowerCase(),
                    text: (el.textContent || '').slice(0, 50).trim(),
                });
            });

            // Find elements with aria-label
            document.querySelectorAll('[aria-label]').forEach(el => {
                elements.push({
                    type: 'aria-label',
                    selector: `[aria-label="${el.getAttribute('aria-label')}"]`,
                    tag: el.tagName.toLowerCase(),
                    text: (el.textContent || '').slice(0, 50).trim(),
                });
            });

            // Find links with href
            document.querySelectorAll('a[href]').forEach(el => {
                const href = el.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                    elements.push({
                        type: 'href',
                        selector: `a[href="${href}"]`,
                        tag: 'a',
                        text: (el.textContent || '').slice(0, 50).trim(),
                    });
                }
            });

            // Find buttons
            document.querySelectorAll('button').forEach(el => {
                const text = (el.textContent || '').trim();
                if (text && text.length < 30) {
                    elements.push({
                        type: 'button',
                        selector: `button:has-text("${text}")`,
                        tag: 'button',
                        text: text,
                    });
                }
            });

            // Find inputs with placeholders
            document.querySelectorAll('input[placeholder]').forEach(el => {
                elements.push({
                    type: 'placeholder',
                    selector: `input[placeholder="${el.getAttribute('placeholder')}"]`,
                    tag: 'input',
                    text: el.getAttribute('placeholder'),
                });
            });

            return elements;
        });

        // Print results grouped by type
        console.log('━'.repeat(60));
        console.log('DISCOVERED SELECTORS');
        console.log('━'.repeat(60));

        const grouped = {};
        selectors.forEach(s => {
            if (!grouped[s.type]) grouped[s.type] = [];
            grouped[s.type].push(s);
        });

        for (const [type, items] of Object.entries(grouped)) {
            console.log(`\n## ${type.toUpperCase()} (${items.length})\n`);
            items.slice(0, 20).forEach(item => {
                console.log(`  ${item.selector}`);
                if (item.text) console.log(`    └─ "${item.text}"`);
            });
            if (items.length > 20) {
                console.log(`  ... and ${items.length - 20} more`);
            }
        }

        console.log('\n━'.repeat(60));
        console.log('Browser will stay open. Press Ctrl+C when done inspecting.');
        console.log('━'.repeat(60));

        // Keep browser open for manual inspection
        await page.waitForTimeout(300000); // 5 minutes

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await context.close();
    }
}

const url = process.argv[2] || 'https://learn.grafana-ops.net/a/grafana-adaptive-metrics-app/overview';
discoverSelectors(url);