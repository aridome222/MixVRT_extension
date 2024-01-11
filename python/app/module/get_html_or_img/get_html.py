# いらないファイルかも
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


# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


# HTMLコードの保存を行う関数
def save_html_data(file_name, html_data):
  ### HTMLデータをhtmlファイルに出力する ###

  # 保存先ディレクトリを指定
  output_dir = os.path.join(diff_dir, "html_data/")
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


def get_html(url, html_file_name):
    """ 
    main処理 
    
    htmlコードを取得する
    """

    response = requests.get(url)
    html_content = response.text  # HTML コンテンツを文字列として取得
    save_html_data(html_file_name, html_content)
