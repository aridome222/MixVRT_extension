from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re
import os
import stat
import glob

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def process_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # soup = BeautifulSoup(soup.prettify(), 'html.parser')

    # 処理するタグのリスト
    tags_to_process = ['p']

    for tag_name in tags_to_process:
        for tag in soup.find_all(tag_name):
            tag.string = ' '.join(tag.get_text().split())

    return str(soup)

def save_diff_html_data(html_data_file, html_data_file_2):
    # HTMLデータの読み込みと処理
    with open(html_data_file, 'r', encoding='utf-8') as file:
        html_content_1 = process_html(file.read())

    with open(html_data_file_2, 'r', encoding='utf-8') as file:
        html_content_2 = process_html(file.read())

    ### ２つのHTMLデータの差分をtxtファイルに出力する ###
    output_dir = os.path.join(diff_dir, "html_diff/")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        subprocess.call(command, shell=True)

    output_file_name = "diff_html.txt"
    output_file_path = os.path.join(output_dir, output_file_name)

    differ = difflib.Differ()
    diff = differ.compare(html_content_1.splitlines(), html_content_2.splitlines())

    with open(output_file_path, "w", encoding="utf-8") as f:
        for line in diff:
            if not line.startswith('?'):
                f.write(line + "\n")
        subprocess.run(['sudo', 'chown', 'aridome:aridome', output_file_path])

    print(f"2つのHTMLデータの差異を{output_file_path}に保存しました")

    return output_file_path


def get_html_path_from_dir(dir):
    # 指定ディレクトリ内のすべての '.html' ファイルのリストを取得
    html_files = glob.glob(os.path.join(dir, '**', '*.html'), recursive=True)

    # ファイルが見つかった場合、最初のファイルのパスを使用
    if html_files:
        first_html_file = html_files[0]
        print("Found HTML file:", first_html_file)
        return first_html_file
    else:
        print("No HTML files found in the directory.")
        return None


""" main処理 """
def gen_diff_html(current_dir, new_data_dir):
    before_file_path = get_html_path_from_dir(current_dir)
    after_file_path = get_html_path_from_dir(new_data_dir)

    return save_diff_html_data(before_file_path, after_file_path)
