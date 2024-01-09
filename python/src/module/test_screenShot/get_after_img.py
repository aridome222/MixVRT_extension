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


def setup_driver():
  options = Options()
  # options.add_argument('--headless')  # ヘッドレスモードでブラウザを起動
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
  driver.implicitly_wait(10)
  return driver

def teardown_driver(driver):
  driver.quit()

# Webページの画像の保存を行う関数
def save_screenShot(driver):
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
  output_file_name = f"SLT_view_b4_{current_date}.png"

  # ファイルパスを作成
  output_file_path = os.path.join(output_dir, output_file_name)

  # スクロールバーが表示されないようにサイズを設定
  driver.set_window_size(1050, 1150) # 幅×高さ

  # 追加: ここでフルページのスクリーンショットを取る
  driver.save_screenshot(output_file_path)

  print("")
  print(f"単一行テキストの配置画像を{output_file_path}に保存しました")


def get_before_img(driver):
    """ 
    main処理 
    
    変更前のwebページ画面の画像を取得する
    """
    url = "http://host.docker.internal:5000/after"

    driver.get(url)
    driver.set_window_size(1463, 1032)

    time.sleep(1)
    save_screenShot(driver)

    # 画面を閉じる
    driver.close()


# スクリプトのエントリーポイント
if __name__ == "__main__":
    driver = setup_driver()
    try:
        # ここにメインの処理を書く
        get_before_img(driver)
    finally:
        teardown_driver(driver)
