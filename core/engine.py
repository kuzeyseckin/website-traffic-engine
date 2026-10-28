import asyncio
import random
from playwright.async_api import async_playwright
from fake_useragent import UserAgent

from core.proxy_parser import ProxyParser
from core.interceptor import TrafficInterceptor


class SimulatorEngine:

    BROWSER_ARGS = [
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-sync",
        "--disable-translate",
        "--mute-audio",
        "--blink-settings=imagesEnabled=false",
        "--no-pings",
        "--disable-component-update",
        "--disable-domain-reliability",
        "--disable-breakpad",
        "--no-first-run",
        "--safebrowsing-disable-auto-update"
    ]

    def __init__(self, log_callback, on_finish_callback):
        self.log = log_callback
        self.on_finish = on_finish_callback

    def run_async_loop(self, url, proxies, duration, max_tabs, loop_count, headless):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            self.main_simulator_logic(url, proxies, duration, max_tabs, loop_count, headless)
        )
        self.on_finish()

    async def visit_page(self, browser, url, proxy_line, duration, task_id):
        proxy_settings, proxy_display = ProxyParser.parse(proxy_line)

        context = None
        try:
            ua = UserAgent()
            viewport = {
                "width": random.choice([1280, 1366, 1440, 1920]),
                "height": random.choice([720, 768, 900, 1080])
            }
            referer_url = random.choice([
                "https://www.google.com/",
                "https://www.reddit.com/",
                "https://t.co/"
            ])

            context = await browser.new_context(
                proxy=proxy_settings,
                viewport=viewport,
                user_agent=ua.random,
                locale=random.choice(['en-US', 'en-GB', 'tr-TR', 'de-DE']),
                timezone_id=random.choice(['America/New_York', 'Europe/London', 'Europe/Istanbul', 'Europe/Berlin']),
                extra_http_headers={"Referer": referer_url}
            )
            page = await context.new_page()

            interceptor = TrafficInterceptor(url)
            await page.route("**/*", interceptor.strict_traffic_saver)

            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            await page.evaluate("window.scrollBy(0, Math.floor(Math.random() * 400) + 300)")
            await page.wait_for_timeout(2000)
            await page.evaluate("window.scrollBy(0, Math.floor(Math.random() * 400) + 300)")

            await page.wait_for_timeout(duration * 1000)
            self.log(f"[#{task_id} SUCCESS] {proxy_display} ({duration} sec)")

        except Exception as e:
            self.log(f"[#{task_id} ERROR] {proxy_display}: {str(e)[:45]}")
        finally:
            if context:
                await context.close()

    async def main_simulator_logic(self, url, proxies, duration, max_tabs, loop_count, headless):
        queue = asyncio.Queue()
        task_id = 0

        for _ in range(loop_count):
            for proxy in proxies:
                task_id += 1
                queue.put_nowait((task_id, proxy))

        total_tasks = queue.qsize()
        self.log(f"[INFO] Prepared {total_tasks} total visit tasks. Concurrent tabs: {max_tabs}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=headless,
                args=self.BROWSER_ARGS
            )

            async def worker():
                while not queue.empty():
                    try:
                        current_id, current_proxy = queue.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    await self.visit_page(browser, url, current_proxy, duration, current_id)
                    queue.task_done()

            workers = [asyncio.create_task(worker()) for _ in range(max_tabs)]
            await asyncio.gather(*workers)
            await browser.close()