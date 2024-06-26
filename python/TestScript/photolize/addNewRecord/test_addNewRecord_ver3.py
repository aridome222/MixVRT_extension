# 完全なXPath指定+HTML解析+属性取得
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


class TestAddNewRecord_ver3():
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
  
  def test_addNewRecord(self):
    self.driver.get("https://saruya:saruya@staging-user.photolize.jp/login/basic_auth")
    self.driver.get("https://staging-user.photolize.jp/login")
    self.driver.set_window_size(1463, 1032)
    self.driver.find_element(By.ID, "input-7").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.ID, "input-7").send_keys("company_code26")
    self.driver.find_element(By.CSS_SELECTOR, ".v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.ID, "input-11").send_keys("aridome")
    self.driver.find_element(By.ID, "input-14").send_keys("aridome")
    element = self.driver.find_element(By.CSS_SELECTOR, ".btn > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".btn > .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".py-0:nth-child(2) .relative")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.execute_script("window.scrollTo(0,317)")
    element = self.driver.find_element(By.CSS_SELECTOR, ".py-0:nth-child(12) .v-list-item__title")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".py-0:nth-child(12) .v-list-item__title").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.LINK_TEXT, "新規レコード追加").click()
    # time.sleep(25)
    # ページソースを取得
    page_source = self.driver.page_source

    # BeautifulSoupを使ってbody部分のみを抽出
    soup = BeautifulSoup(page_source, 'html.parser')
    body_content = soup.body

    # 正規表現オブジェクトを作成
    pattern = re.compile("input-221")

    # bodyから正規表現に一致するテキストを含む要素をすべて取得
    matches = body_content.find_all(attrs={"id": pattern})

    # 結果が表示されるかどうかで違う処理を行う
    if matches: # 結果が表示される場合
        print("一致する要素が見つかりました")
        for match in matches:
            print(match)
    else: # 結果が表示されない場合
        print("一致する要素が見つかりませんでした")
        pattern = re.compile("input-")
        matches = body_content.find_all(attrs={"id": pattern})
        for match in matches:
            print(match)

    element = self.driver.find_element(By.CSS_SELECTOR, ".input").click()
    # html = element.get_attribute('id')
    # time.sleep(15)
    # 指定したIDの要素がクリック可能になるまで待機
    # element = self.driver.find_element(By.ID, "input-221")
    element = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div[6]/div/div/div[1]/div/span/span/div/div/div[1]/div/input")
    self.driver.execute_script("arguments[0].click();", element)
    # wait = WebDriverWait(self.driver, 10)
    # element = wait.until(EC.element_to_be_clickable((By.ID, "input-221")))
    # 要素のhtmlを取得
    html = element.get_attribute('id')
    # assert html == '<input id="input-221" type="text">'
    print(html)
    # element.click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-dialog__content:nth-child(6) .v-card__actions .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div[6]/div/div/div[1]/div/span/span/div/div/div[1]/div/input")
    # キーボードのショートカットで入力内容を全選択
    element.send_keys(Keys.CONTROL + "a")
    # キーボードのショートカットで入力内容を削除
    element.send_keys(Keys.DELETE)
    time.sleep(2)
    element.send_keys("お寿司")
    self.driver.find_element(By.CSS_SELECTOR, ".v-dialog__content:nth-child(6) .v-card__actions .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".checkbox").click()
    self.driver.execute_script("window.scrollTo(0,200)")
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .cbbox").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .cbbox")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .cbbox").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-dialog__content:nth-child(16) .v-card__actions .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-dialog__content:nth-child(16) .v-card__actions .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".radio").click()
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".v-radio:nth-child(3) .v-input--selection-controls__ripple").click()
    self.driver.find_element(By.CSS_SELECTOR, ".v-dialog__content:nth-child(10) .v-card__actions .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn--is-elevated > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-btn--is-elevated > .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".theme--light:nth-child(2) > .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".theme--light:nth-child(2) > .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-card__actions:nth-child(2) .v-btn__content")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-card__actions:nth-child(2) .v-btn__content").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-avatar > img")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-avatar > img").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".v-btn--text")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".v-btn--text").click()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.close()
  
