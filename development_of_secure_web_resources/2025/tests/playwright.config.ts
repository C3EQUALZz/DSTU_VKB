import { defineConfig, devices } from '@playwright/test';

// Локальные лабы запускаются через python3 -m http.server из корня
// каталога 2025. Каждая лаба доступна по адресу http://127.0.0.1:8800/<N>/...
export default defineConfig({
    testDir: '.',
    timeout: 30_000,
    fullyParallel: false,
    use: {
        baseURL: 'http://127.0.0.1:8800',
        actionTimeout: 5_000,
        navigationTimeout: 10_000,
    },
    reporter: process.env.CI ? 'list' : 'list',
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
    webServer: {
        command: 'python3 -m http.server 8800 --bind 127.0.0.1',
        cwd: '..',
        url: 'http://127.0.0.1:8800/',
        reuseExistingServer: !process.env.CI,
        timeout: 15_000,
        stdout: 'ignore',
        stderr: 'pipe',
    },
});
