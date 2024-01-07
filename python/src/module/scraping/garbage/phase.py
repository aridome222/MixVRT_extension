from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


# 保存先ディレクトリを指定
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

diff_file_path = os.path.join(input_dir, "diff_html.txt")

# テキストファイル読み込み
with open(diff_file_path, 'r') as file:
    lines = file.readlines()

# 各フェーズの内容を格納する変数を初期化
phase_1_content = []
phase_2_content = []
phase_3_content = []
phase_4_content = []

# 現在のフェーズを追跡する変数
current_phase = 1

# 各行をチェックして、フェーズに応じて内容を分割
for line in lines:
    if '<head>' in line:
        current_phase = 2
    elif '</head>' in line:
        current_phase = 3
    elif '<body>' in line:
        current_phase = 3
    elif '</body>' in line:
        current_phase = 4

    # 各フェーズに内容を追加
    if current_phase == 1:
        phase_1_content.append(line)
    elif current_phase == 2:
        phase_2_content.append(line)
    elif current_phase == 3:
        phase_3_content.append(line)
    elif current_phase == 4:
        phase_4_content.append(line)

# 各フェーズの内容を処理するための関数
def process_phase_1(content):
    # フェーズ1の処理を実装
    pass

def process_phase_2(content):
    # フェーズ2の処理を実装
    pass

def process_phase_3(content):
    # フェーズ3の処理を実装
    pass

def process_phase_4(content):
    # フェーズ4の処理を実装
    pass

# 各フェーズの内容を処理
process_phase_1(phase_1_content)
process_phase_2(phase_2_content)
process_phase_3(phase_3_content)
process_phase_4(phase_4_content)