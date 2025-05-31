class CheckOut():
    def __init__(self, page):
        self.page = page

    async def complete_purchase(self):
        await self.page.click("text=결제하기")
        await self.page.wait_for_selector("text=주문완료")