# htmlを解析して情報を取得する
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
import subprocess


class Test_slt_input_addShot():
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
    # photolizeにログインする
    self.driver.get("https://saruya:saruya@staging-user.photolize.jp/login/basic_auth")
    self.driver.get("https://staging-user.photolize.jp/login")
    self.driver.set_window_size(1463, 1032)
    self.driver.find_element(By.ID, "input-7").click()
    self.driver.find_element(By.ID, "input-7").send_keys("company_code26")
    self.driver.find_element(By.CSS_SELECTOR, ".v-btn__content").click()
    self.driver.find_element(By.ID, "input-11").send_keys("aridome")
    self.driver.find_element(By.ID, "input-14").send_keys("aridome")
    self.driver.find_element(By.CSS_SELECTOR, ".btn > .v-btn__content").click()

    ## 有留アプリテストを選択
    # 直接飛ぶ
    self.driver.get("https://staging-user.photolize.jp/appli/index?app_id=151")
    # 新規レコードの編集を選択
    self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div/a/span/i").click()
    
    

    # 画面を閉じる
    self.driver.close()

def save_screenShot(self):
  # 保存先ディレクトリを指定
  output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")
  # フォルダが存在しない場合は作成
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)
      command = f"sudo chown -R aridome:aridome {output_dir}"
      # コマンドを実行
      subprocess.call(command, shell=True)

  # 現在の日付を取得してフォーマット
  current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
  # ファイル名を生成
  output_file_name = f"SLT_view_af_{current_date}.png"

  # ファイルパスを作成
  output_file_path = os.path.join(output_dir, output_file_name)
  
  # スクロールバーが表示されないようにサイズを設定
  self.driver.set_window_size(1050, 1150) # 幅×高さ

  # 追加: ここでフルページのスクリーンショットを取る
  self.driver.save_screenshot(output_file_path)

  print("")
  print(f"単一行テキストの配置画像を{output_file_path}に保存しました")