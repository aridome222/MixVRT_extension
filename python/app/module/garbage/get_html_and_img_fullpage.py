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
import requests
import argparse


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

def save_screenShot(driver, dir):
    # 保存先ディレクトリを指定
    output_dir = os.path.join(dir, "img/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)
    # 現在の日付を取得してフォーマット
    current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
    # ファイル名を生成
    output_file_name = f"img_{current_date}.png"

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir, output_file_name)

    # 新しい部分: ページの全高さを取得
    total_height = driver.execute_script("return document.body.scrollHeight")

    # ブラウザの画面サイズを取得
    window_height = driver.get_window_size()["height"]

    # ページの初めから最後までスクロール
    for i in range(0, total_height, window_height):
        # スクロール
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)  # スクロールの安定化のための待機

    # スクロールが完了したらスクリーンショットを撮る
    driver.save_screenshot(output_file_path)

    print(f"フルページのスクリーンショットを{output_file_path}に保存しました")


# HTMLコードの保存を行う関数
def save_html_data(html_data, dir):
  ### HTMLデータをhtmlファイルに出力する ###

  # 保存先ディレクトリを指定
  output_dir = os.path.join(dir, "html/")
  # フォルダが存在しない場合は作成
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)
      command = f"sudo chown -R aridome:aridome {output_dir}"
      # コマンドを実行
      subprocess.call(command, shell=True)
      
  # 現在の日付を取得してフォーマット
  current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  # ファイル名を生成
  output_file_name = f"html_{current_date}.html"
  
  # ファイルにHTMLデータを出力
  output_file_path = os.path.join(output_dir, output_file_name)
  with open(output_file_path, "w", encoding="utf-8") as f:
      f.write(html_data)
      subprocess.run(['sudo', 'chown', 'aridome:aridome', output_file_path])

  print(f"HTMLデータを{output_file_path}に保存しました")


def get_html_and_img(driver, url, dir):
    """ 
    変更前のwebページ画面の画像を取得する
    """
    # # WebページのURL
    # url = "http://host.docker.internal:5000/testPage"

    # 画像取得
    driver.get(url)
    driver.set_window_size(1463, 1032)
    save_screenShot(driver, dir)

    # HTMLコード取得
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック
    html_content = response.text  # HTML コンテンツを文字列として取得
    save_html_data(html_content, dir)

    # 画面を閉じる
    driver.close()


def main(dir, url):
    driver = setup_driver()
    try:
        get_html_and_img(driver, url, dir)
    finally:
        teardown_driver(driver)
