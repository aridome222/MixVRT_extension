# 追加・削除・変更されたセレクタ名を取得するための関数
from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


def apply_style_to_changes(diff_file_path):
    with open(diff_file_path, 'r') as file:
        diff_lines = file.readlines()

    changed_selectors = []

    inside_style_tag = False
    for line in diff_lines:
        if '<style>' in line:
            inside_style_tag = True
            continue
        elif '</style>' in line:
            inside_style_tag = False
            continue

        if inside_style_tag and '{' in line:
            current_selector = line.split('{')[0].strip().strip('+').strip('-').strip()

            if line.startswith('+') or line.startswith('-'):
                if current_selector not in changed_selectors:
                    changed_selectors.append(current_selector)

    return changed_selectors


""" main処理 """
# 保存先ディレクトリを指定
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

diff_file_path = os.path.join(input_dir, "diff_html.txt")

changed_selectors = apply_style_to_changes(diff_file_path)

### 検証用のprint文 ###
print(f"changed_selectors:\n {changed_selectors}")
