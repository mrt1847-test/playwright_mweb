class MyG():
    def __init__(self, page):
        self.page = page

    async def verify_latest_order(self):
        await self.page.goto("https://m.gmarket.co.kr/mypage/orderlist")
        assert await self.page.is_visible("text=무선 이어폰")