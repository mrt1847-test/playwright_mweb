# tests/test_gmarket_purchase_flow.py
import pytest
import pydata_google_auth
import gspread
import json
import os
import platform

from src.login_page import Login
from src.srp_page import Srp
from src.vip_page import Vip
from src.checkout_page import CheckOut
from src.myg_page import MyG

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
credentials = pydata_google_auth.get_user_credentials(SCOPES, auth_local_webserver=True)
credentials.access_token = credentials.token
gc = gspread.authorize(credentials)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Hmrpoz1EVACFY5lHW7r4v8bEtRRFu8eay7grCojRr3E/edit?gid=0#gid=0"
sh = gc.open_by_url(spreadsheet_url)
worksheet = sh.worksheet("tc1")
os_version = platform.platform()
if 'Windows' in os_version:  # windows인 경우
    param_json_path = os.path.dirname(__file__) + '\\json\\'
    current_json = param_json_path + os.path.splitext(os.path.basename(__file__))[0] + '.json'
elif 'mac' in os_version:
    param_json_path = os.path.dirname(__file__) + '/json/'
    current_json = param_json_path + os.path.splitext(os.path.basename(__file__))[0] + '.json'

with open(current_json, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

def input_pass(test_id,sheet_num):
    worksheet = sh.worksheet(test_id)
    if json_data[0]["tc{0}".format(sheet_num)]["use_type"] == 2:
        worksheet.update([["pass"]], f"D{sheet_num+2}")
        worksheet.format(f"D{sheet_num+2}", {"textFormat": {"foregroundColor": {"red": 0.0, "green": 0.5, "blue": 0.0}, "bold": True}})
        worksheet.update([[" "]], f"E{sheet_num+2}")
    else:
        worksheet.update([["untest"]], f"D{sheet_num+2}")
        worksheet.format(f"D{sheet_num+2}",
                     {"textFormat": {"foregroundColor": {"red": 0.5, "green": 0.5, "blue": 0.5}, "bold": True}})
        worksheet.update([[" "]], f"E{sheet_num+2}")
def input_fail(test_id, sheet_num, error_reason):
    worksheet = sh.worksheet(test_id)
    worksheet.update([["fail"]], f"D{sheet_num+2}")
    worksheet.format(f"D{sheet_num+2}", {"textFormat": {"foregroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}, "bold": True}})
    worksheet.update([[str(error_reason)]], f"E{sheet_num+2}")

#pipenv run pytest --cache-clear test.py --asyncio-mode=auto -n 4
@pytest.mark.asyncio
async def test(page,request):
    test_id = request.node.name
    login = Login(page)
    search = Srp(page)
    product = Vip(page)
    order = CheckOut(page)
    mypage = MyG(page)
    try:
        await login.goto()
        await login.login("cease2504", "")

        await search.search_product("무선 이어폰")
        await product.select_first_product()
        await product.click_buy_now()

        await order.complete_purchase()
        await mypage.verify_latest_order()
        input_pass(test_id,1)
    except Exception as e:
        await page.screenshot(path="error_screenshot.png")
        input_fail(test_id,2, e)
        raise e  # 테스트를 실패로 처리