# "+"にしか対応していない、+がcssセレクタの前の行にあると、
# そのcssセレクタが変更されていないのにもかかわらず、
# 変更されたセレクタと判定されてしまう
from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


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

selectors = apply_style_to_changes(diff_file_path)

### 検証用のprint文 ###
print(selectors)
