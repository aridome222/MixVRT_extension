from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


def apply_style_to_changes(diff_file_path):
    with open(diff_file_path, 'r') as file:
        diff_lines = file.readlines()

    added_selectors = []
    deleted_selectors = []

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

            if line.startswith('+') and current_selector not in added_selectors:
                added_selectors.append(current_selector)
            elif line.startswith('-') and current_selector not in deleted_selectors:
                deleted_selectors.append(current_selector)

    return added_selectors, deleted_selectors


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

added_selectors, deleted_selectors = apply_style_to_changes(diff_file_path)

### 検証用のprint文 ###
print(f"added_selectors:\n {added_selectors}")
print(f"deleted_selectors:\n {deleted_selectors}")
