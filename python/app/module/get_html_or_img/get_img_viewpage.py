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

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


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
def save_screenShot(driver, modified_file_path):
  # 保存先ディレクトリを指定
  output_dir = os.path.join(diff_dir, "img_of_modified_html/")
  # フォルダが存在しない場合は作成
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)
      command = f"sudo chown -R aridome:aridome {output_dir}"
      # コマンドを実行
      subprocess.call(command, shell=True)

  # ファイル名を生成
  output_file_name = os.path.basename(modified_file_path).split(".")[0] + '.png'

  # ファイルパスを作成
  output_file_path = os.path.join(output_dir, output_file_name)

  # # スクロールバーが表示されないようにサイズを設定
  # driver.set_window_size(1050, 1150) # 幅×高さ

  time.sleep(0.5)

  # 追加: ここでフルページのスクリーンショットを取る
  driver.save_screenshot(output_file_path)
  
  print("")
  print(f"枠処理された画像を{output_file_path}に保存しました")
  
  return output_file_path


def get_img(driver, url, modified_file_path):
    """ 
    main処理 
    
    webページ画面の画像を取得する
    """
    driver.get(url)
    driver.set_window_size(1463, 1032)

    img_path = save_screenShot(driver, modified_file_path)

    # 画面を閉じる
    driver.close()

    return img_path


def main(url, modified_file_path):
    driver = setup_driver()
    try:
        img_path = get_img(driver, url, modified_file_path)
    finally:
        teardown_driver(driver)

    return img_path

