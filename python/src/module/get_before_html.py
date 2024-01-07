from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import subprocess
import difflib

# 省略（setup_methodに相当する処理）
def setup_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
    driver.implicitly_wait(10)
    return driver

# 省略（teardown_methodに相当する処理）
def teardown_driver(driver):
    driver.quit()

def addNewRecord(self):
    self.driver.get("http://host.docker.internal:5000/before")
    self.driver.set_window_size(1463, 1032)

    url = "http://host.docker.internal:5000/before"
    response = requests.get(url)
    html_content = response.text  # HTML コンテンツを文字列として取得
    save_html_data("before", html_content)

    # 画面を閉じる
    self.driver.close()

# スクリプトのエントリーポイント
if __name__ == "__main__":
    driver = setup_driver()
    try:
        # ここにメインの処理を書く
        addNewRecord(driver)
    finally:
        teardown_driver(driver)
