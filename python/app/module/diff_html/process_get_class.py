from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def apply_style_to_changes(diff_file_path):
    with open(diff_file_path, 'r') as file:
        diff_lines = file.readlines()

    changed_selectors = []
    current_selector = None

    for line in diff_lines:
        if '{' in line:
            selector = line.split('{')[0].strip().strip('+').strip('-').strip()
            if line.startswith('+') or line.startswith('-'):
                if selector not in changed_selectors:
                    changed_selectors.append(selector)
            current_selector = selector
            continue

        if '}' in line:
            current_selector = None
            continue

        if current_selector is not None and (line.startswith('+') or line.startswith('-')):
            if current_selector not in changed_selectors:
                changed_selectors.append(current_selector)

    return changed_selectors


""" main処理 """
# 保存先ディレクトリを指定
input_dir = os.path.join(diff_dir, "html_diff/")

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
