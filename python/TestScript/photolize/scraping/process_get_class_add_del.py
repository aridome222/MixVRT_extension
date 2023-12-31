from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


def apply_style_to_changes(diff_file_path):
    # テキストファイルからスタイル情報を読み込む
    with open(diff_file_path, 'r') as file:
        diff_lines = file.readlines()

    # 変更されたセレクタを格納するリスト
    added_selectors = []
    deleted_selectors = []

    # <style> タグ内のスタイル情報を行単位で処理
    inside_style_tag = False
    current_selector = None
    for line in diff_lines:
        if '<style>' in line:
            inside_style_tag = True
            continue
        elif '</style>' in line:
            inside_style_tag = False
            current_selector = None  # Reset current selector
            continue

        if inside_style_tag:
            if '{' in line:
                # 新しいセレクタを取得
                current_selector = line.split('{')[0].strip().lstrip('+').lstrip('-').strip()
                continue  # Skip to the next line

            if current_selector:
                if line.startswith('+'):
                    # 追加されたセレクタを処理
                    if current_selector not in added_selectors:
                        added_selectors.append(current_selector)
                elif line.startswith('-'):
                    # 削除されたセレクタを処理
                    if current_selector not in deleted_selectors:
                        deleted_selectors.append(current_selector)

                # Reset current selector if the CSS block ends
                if '}' in line:
                    current_selector = None

    return added_selectors, deleted_selectors



# 保存先ディレクトリを指定
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

before_file_name = "before.html"
after_file_name = "after.html"

before_file_path = os.path.join(output_dir, before_file_name)
after_file_path = os.path.join(output_dir, after_file_name)

# HTMLファイルを読み込む
with open(before_file_path, 'r') as file:
    before_html = file.read()

with open(after_file_path, 'r') as file:
    after_html = file.read()

# 保存先ディレクトリを指定
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

diff_file_path = os.path.join(input_dir, "diff_html.txt")

# # 余分な // を 1 つの / に変更する処理
# if diff_file_path.startswith('//'):
#     diff_file_path = '/' + diff_file_path.lstrip('/')

added_selectors, deleted_selectors = apply_style_to_changes(diff_file_path)
print(f"added_selectors:\n {added_selectors}")
print(f"deleted_selectors:\n {deleted_selectors}")

# before_modified_html, after_modified_html = apply_style_to_changes(before_html, after_html)

# before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
# after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# # print(after_modified_html)

# # 変更されたHTMLをファイルに書き出す
# with open(before_modified_file_path, 'w') as file:
#     file.write(before_modified_html)

# with open(after_modified_file_path, 'w') as file:
#     file.write(after_modified_html)

def add_style_changed_class(html_file_path, changed_selectors):
    # HTMLファイルを読み込む
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    # 変更されたセレクタに対応する要素を見つけてクラスを追加
    for selector in changed_selectors:
        for element in soup.select(selector):
            element['class'] = element.get('class', []) + ['style-changed']

    # 変更されたHTMLコンテンツをファイルに書き戻す
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))