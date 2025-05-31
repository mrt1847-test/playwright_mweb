# tests/test_gmarket_purchase_flow.py
import pytest
from src.login_page import Login
from src.SrpPage import Srp
from src.VipPage import Vip
from src.CheckOutPage import CheckOut
from src.MyGPage import MyG

#pipenv run pytest --cache-clear test.py --asyncio-mode=auto -n 4
@pytest.mark.asyncio
async def test_gmarket_purchase_flow(page):
    login = Login(page)
    search = Srp(page)
    product = Vip(page)
    order = CheckOut(page)
    mypage = MyG(page)

    await login.goto()
    await login.login("cease2504", "")

    await search.search_product("무선 이어폰")
    await product.select_first_product()
    await product.click_buy_now()

    await order.complete_purchase()
    await mypage.verify_latest_order()