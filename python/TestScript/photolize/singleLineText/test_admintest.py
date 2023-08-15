# 単一行テキストの配置テスト
# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.keys import Keys
import json
import os
from datetime import datetime
import difflib


class TestAdmintest():
  def setup_method(self, method):
    options = Options()
    # options.add_argument('--headless')  # ヘッドレスモードでブラウザを起動
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    self.driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
    self.driver.implicitly_wait(10) # 10秒まで待機する
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_singlelinetext(self):    
    # photolize管理画面にログインする
    self.driver.get("https://saruya:saruya@staging-admin.photolize.jp/login")
    self.driver.set_window_size(1463, 1032)
    self.driver.find_element(By.ID, "admin_user_code").send_keys("admin_test")
    self.driver.find_element(By.ID, "password").send_keys("31g8ar7p")
    self.driver.find_element(By.CSS_SELECTOR, ".uk-button").click()
    # 有留テストアプリに移動する
    self.driver.find_element(By.LINK_TEXT, "アプリ一覧を見る").click()
    # self.driver.find_element(By.LINK_TEXT, "有留テストアプリ").click()
    # self.driver.find_element(By.LINK_TEXT, "有留テストアプリ").click() # この行をコメントアウトする
    element = self.driver.find_element(By.LINK_TEXT, "有留テストアプリ") # この行を追加する
    actions = ActionChains(self.driver) # この行を追加する
    actions.move_to_element(element).click().perform() # この行を追加する
    # いろいろ操作
    self.driver.find_element(By.XPATH, "//div[4]/div/div/div").click()
    self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".selectedDraggable")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".selectedDraggable")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".selectedDraggable")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.CSS_SELECTOR, ".selectedDraggable").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) select").click()
    dropdown = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) select")
    dropdown.find_element(By.XPATH, "//option[. = 'センター中央寄せ']").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) select").click()
    dropdown = self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) select")
    dropdown.find_element(By.XPATH, "//option[. = '8']").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > td > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) > td > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(5) > td > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) label > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) label > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(5) label > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(6) .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("1")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("3")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("4")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("5")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").send_keys("6")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(1) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").send_keys("1")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").send_keys("3")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").click()
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").send_keys("4")
    self.driver.find_element(By.CSS_SELECTOR, ".toolbar-position-inp:nth-child(2) > .small").click()
    dragged = self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .drag-item")
    dropped = self.driver.find_element(By.CSS_SELECTOR, ".v-responsive__content")
    actions = ActionChains(self.driver)
    actions.drag_and_drop(dragged, dropped).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn:nth-child(5)")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn:nth-child(7) > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn:nth-child(9) > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-app-bar__nav-icon > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-app-bar__nav-icon > .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element, 0, 0).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-list-item:nth-child(1) > .v-list-item__title").click()
    assert self.driver.switch_to.alert.text == "アプリ一覧にもどってもよろしいでしょうか？保存されていないデータは消失します。"
    self.driver.switch_to.alert.accept()
    # ログアウトして画面を閉じる
    self.driver.find_element(By.LINK_TEXT, "テストマニュアル管理者").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()