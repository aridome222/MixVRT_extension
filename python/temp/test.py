from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import regex
from selenium.webdriver.common.keys import Keys
import json
import os
from datetime import datetime
import difflib
import subprocess

# WebDriverの初期化
chrome_driver_path = "C:\\Users\\N.aridome\\Downloads\\chromedriver_win32"  # Chromeドライバーの実行可能ファイルへのパス
# WebDriverの初期化
driver = webdriver.Chrome()


# デバイスのディスプレイサイズを取得
driver.get("https://saruya:saruya@staging-user.photolize.jp/login/basic_auth")
driver.get("https://staging-user.photolize.jp/login")
driver.set_window_size(1463, 1039)
driver.find_element(By.ID, "input-7").click()

x = 950
y = 560
actions = ActionChains(driver)
actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), x, y).click().perform()
time.sleep(2)

# ここでウィンドウサイズがディスプレイサイズに設定されたウィンドウが表示されます

# テスト実行などの後にWebDriverをクローズ
driver.quit()
