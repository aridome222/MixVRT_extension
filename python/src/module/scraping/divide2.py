from bs4 import BeautifulSoup
from html.parser import HTMLParser
from difflib import Differ
from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re
import os
import stat

def process_html_file(html_content):

    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    soup = BeautifulSoup(soup.prettify(), 'html.parser')

    # 各<p>タグを見つけて処理
    for p in soup.find_all('p'):
        # 各<p>タグ内のテキストを一行に結合
        p.string = ' '.join(p.get_text().split())


    ### 編集したファイルの保存 ###
    # 保存先ディレクトリを指定
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # 編集したHTMLを保存（拡張子を.htmlにする）
    modified_before_file_path = os.path.join(output_dir, "test1.html")

    # 変更されたHTMLをファイルに書き込む
    with open(modified_before_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    # 変更されたHTMLを文字列として返す
    return str(soup)

# 保存先ディレクトリを指定
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

before_file_name = "b1.html"
after_file_name = "a1.html"

before_file_path = os.path.join(output_dir, before_file_name)
after_file_path = os.path.join(output_dir, after_file_name)

# HTMLファイルを読み込む
with open(before_file_path, 'r') as file:
    before_html = file.read()

with open(after_file_path, 'r') as file:
    after_html = file.read()


# HTMLファイルを処理
processed_html = process_html_file(after_html)

# 結果を表示（または必要に応じて保存）
print(processed_html)
