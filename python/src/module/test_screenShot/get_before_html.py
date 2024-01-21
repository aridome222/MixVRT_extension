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

import requests


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

# HTMLコードの保存を行う関数
def save_html_data(file_name, html_data):
  ### HTMLデータをhtmlファイルに出力する ###

  # 保存先ディレクトリを指定
  output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
  # フォルダが存在しない場合は作成
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)
      command = f"sudo chown -R aridome:aridome {output_dir}"
      # コマンドを実行
      subprocess.call(command, shell=True)
      
  # # 現在の日付を取得してフォーマット
  # current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  # # ファイル名を生成
  # output_file_name = f"{file_name}_{current_date}.html"
  output_file_name = f"{file_name}.html"
  
  # ファイルにHTMLデータを出力
  output_file_path = os.path.join(output_dir, output_file_name)
  with open(output_file_path, "w", encoding="utf-8") as f:
      f.write(html_data)

  print(f"HTMLデータを{output_file_path}に保存しました")


def get_before_html(driver):
    """ 
    main処理 
    
    変更前のhtmlコードを取得する
    """
    url = "http://host.docker.internal:5000/before"

    response = requests.get(url)
    html_content = response.text  # HTML コンテンツを文字列として取得
    save_html_data("before", html_content)

    # 画面を閉じる
    driver.close()


# スクリプトのエントリーポイント
if __name__ == "__main__":
    driver = setup_driver()
    try:
        # ここにメインの処理を書く
        get_before_html(driver)
    finally:
        teardown_driver(driver)
