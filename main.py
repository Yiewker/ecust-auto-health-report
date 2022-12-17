from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._api_types import TimeoutError as Terror
import os


def run(playwright: Playwright, stu_id, password) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    page.goto(
        "https://sso.ecust.edu.cn/authserver/login?service=https%3A%2F%2Fworkflow.ecust.edu.cn%2Fdefault%2Fwork%2Fuust%2Fzxxsmryb%2Fmrybcn.jsp")
    page.click("#username")
    page.fill("#username", stu_id)
    page.click("#password")
    page.fill("#password", password)
    page.locator('button').click()
    # Click ins
    page.click("ins")
    # Click text=下一步
    page.click("text=下一步")
    
    #以下内容为按钮：
    page.click("#radio_swjkzk17") # 健康状况：健康
    page.click("#radio_xrywz29") # 现人员位置：在上海(33)   徐汇校区（29）
    #page.click("#radio_xcm5") # 行程码是否绿码： 是
    #page.click("#radio_twsfzc9") # 体温是否正常：是
    #page.click("#radio_jkmsflm13") # 健康码是否绿码： 是
    page.click("#radio_sfycxxwc41")# 是否有从学校外出: 否
    
    # Click text=提交
    page.click("text=提交")
    # Click text=确定
    page.click("text=确定")
    # Click text=确定
    page.click("text=确定")
    # ---------------------
    context.close()
    browser.close()


data = os.environ.get('ACCOUNT').strip().split()  # 字符串预处理

for i in range(0, len(data), 2):
    account = data[i]
    password = data[i+1]
    try:
        with sync_playwright() as playwright:
            run(playwright, account.strip(), password.strip())
    except Terror:
        print('健康打卡失败，可能已自行打卡，请注意需自行填写')
        raise
    except Exception as e:
        print(f'健康打卡失败 错误原因{e}')
        raise
    else:
        print('今日已完成健康打卡')
