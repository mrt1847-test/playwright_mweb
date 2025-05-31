
import pytest
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

DEVICE_CONFIGS = {
    "android_chrome": {
        "user_agent": (
            "Mozilla/5.0 (Linux; Android 11; SM-G991B) "
            "Chrome/114.0.5735.196 Mobile Safari/537.36"
        ),
        "viewport": {"width": 412, "height": 915},
        "is_mobile": True,
        "device_scale_factor": 2.5,
        "has_touch": True,
        "locale": "ko-KR"
    },
    "android_firefox": {
        "user_agent": (
            "Mozilla/5.0 (Android 11; Mobile; rv:109.0) "
            "Gecko/109.0 Firefox/109.0"
        ),
        "viewport": {"width": 412, "height": 915},
        "is_mobile": True,
        "device_scale_factor": 2.5,
        "has_touch": True,
        "locale": "ko-KR"
    }
}


@pytest.fixture(scope="function", params=["chromium", "firefox"])
async def browser_type(request):
    async with async_playwright() as p:
        browser_launcher = getattr(p, request.param)
        browser = await browser_launcher.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        yield browser
        await browser.close()


@pytest.fixture(scope="function", params=list(DEVICE_CONFIGS.keys()))
async def context(browser_type: Browser, request) -> BrowserContext:
    device = DEVICE_CONFIGS[request.param]
    context = await browser_type.new_context(
        **device
    )
    # Stealth 우회용 init script
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    yield context
    await context.close()


@pytest.fixture(scope="function")
async def page(context: BrowserContext) -> Page:
    page = await context.new_page()
    page.set_default_timeout(10000)  # 기본 타임아웃 10초
    yield page
    await page.close()