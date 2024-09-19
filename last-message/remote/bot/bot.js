const { chromium } = require('playwright-chromium');
const readline = require('readline');

const FLAG = process.env.FLAG;
const URL = "http://app:8080";

(async function () {
    const browser = await chromium.launch({
        args: ['--ignore-certificate-errors'],
        ignoreHTTPSErrors: true
    });

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    async function start() {
        console.log(`Visiting ${URL}`);

        const context = await browser.newContext({ ignoreHTTPSErrors: true });
        await context.addCookies([{
            name: 'FLAG',
            value: FLAG,
            domain: 'app',
            path: '/'
        }]);

        const page = await context.newPage();

        await page.goto(URL, { waitUntil: 'networkidle' });

        console.log(`Waiting for page to load, this may take a few seconds...`);
        await page.waitForSelector('#username');
        const username = await page.$eval('#username', element => element.innerHTML);
        console.log(`Username: ${username}`);

        setTimeout(() => {
            try {
                page.close();
                console.log('Timeout reached. Closing the page.');
                process.exit(0);
            } catch (err) {
                console.error(`Error: ${err}`);
            }
        }, 30000);
    }

    console.log('The admin will visit the page and send you their username. Press Enter to continue.');

    rl.question('', async () => {
        try {
            await start();
        } catch (err) {
            console.error(`Error: ${err}`);
        } finally {
            rl.close();
        }
    });
})();