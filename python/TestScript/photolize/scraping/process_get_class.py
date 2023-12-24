from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         diff_text = file.read()

#     # <style> タグ内のスタイル情報を抽出
#     start_tag = '<style>'
#     end_tag = '</style>'

#     # スタイル情報を格納するリスト
#     style_list = []

#     # <style> タグ内のスタイル情報を抽出
#     start_idx = diff_text.find(start_tag)
#     end_idx = diff_text.find(end_tag)
#     if start_idx != -1 and end_idx != -1:
#         style_text = diff_text[start_idx + len(start_tag):end_idx].strip()

#         # スタイル情報をセレクタ単位で分割
#         style_rules = style_text.split('}')
#         # 各行を処理してセレクタとスタイル情報を抽出
#         for rule in style_rules:
#             # 行頭の+記号を探す
#             if '+' in rule:
#                 rule = rule.strip()  # 空白を削除
#                 rule = rule.lstrip('+').strip()  # +記号を取り除く
#                 parts = rule.split('{', 1)
#                 if len(parts) == 2:
#                     selector = parts[0].lstrip('+').strip()
#                     styles = parts[1].strip('}').replace('+', '')
#                     style_list.append({'selector': selector, 'style': styles})

#         # 結果の表示
#         for item in style_list:
#             print(f'セレクタ: {item["selector"]}')
#             print(f'スタイル情報: {item["style"]}')
#             print('---')

def apply_style_to_changes(diff_file_path):
    # テキストファイルからスタイル情報を読み込む
    with open(diff_file_path, 'r') as file:
        diff_text = file.read()

    # <style> タグ内のスタイル情報を抽出
    start_tag = '<style>'
    end_tag = '</style>'

    # スタイル情報を格納するリスト
    style_list = []

    # 変更されたセレクタを格納するリスト
    changed_selectors = []

    # <style> タグ内のスタイル情報を抽出
    start_idx = diff_text.find(start_tag)
    end_idx = diff_text.find(end_tag)
    if start_idx != -1 and end_idx != -1:
        style_text = diff_text[start_idx + len(start_tag):end_idx].strip()

        # スタイル情報をセレクタ単位で分割
        style_rules = style_text.split('}')
        # 各行を処理してセレクタとスタイル情報を抽出
        for rule in style_rules:
            # 行頭の+記号を探す
            if '+' in rule:
                rule = rule.strip()  # 空白を削除
                rule = rule.lstrip('+').strip()  # +記号を取り除く
                parts = rule.split('{', 1)
                if len(parts) == 2:
                    selector = parts[0].lstrip('+').strip()
                    styles = parts[1].strip('}').replace('+', '')
                    style_list.append({'selector': selector, 'style': styles})
                    changed_selectors.append(selector)

    return changed_selectors


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

selectors = apply_style_to_changes(diff_file_path)
print(selectors)

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