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
import subprocess


class TestLabelSnapshot:
    def setup_method(self, method):
        options = Options()
        # options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--blink-settings=imagesEnabled=false') 
        self.driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
        self.driver.implicitly_wait(10)
        self.vars = {}

        # 保存先ディレクトリを指定
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mp4/")
        # フォルダが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            command = f"sudo chown -R aridome:aridome {output_dir}"
            # コマンドを実行
            subprocess.call(command, shell=True)

        # 現在の日付を取得してフォーマット
        current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
        # ファイル名を生成
        output_file_name = f"video_{current_date}.mp4"

        # 録画ファイルのパスを設定
        recording_file_path = os.path.join(output_dir, output_file_name)
        # 録画開始
        self.recording_process = start_recording(self.driver.current_window_handle, recording_file_path)

    def teardown_method(self, method):
        # 録画終了
        stop_recording(self.recording_process)

        self.driver.quit()

    def test_example_20231209(self):
        self.driver.get("https://example.com")
        self.driver.set_window_size(1463, 1032)
        time.sleep(3)
        

def start_recording(window_id, output_file):
    command = [
        'ffmpeg',
        '-y',  # 既存のファイルを上書き
        '-f', 'x11grab',  # X11グラブ
        '-i', f':0.0+{window_id}',  # ウィンドウIDを指定
        output_file
    ]
    return subprocess.Popen(command)

def stop_recording(process):
    process.terminate()
    process.wait()