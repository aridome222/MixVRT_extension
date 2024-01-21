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


def save_diff_html_data(html_data_file, html_data_file_2):
    ### ２つのHTMLデータの差分をtxtファイルに出力する ###
    
    # 保存先ディレクトリを指定
    output_dir = os.path.join(diff_dir, "html_diff/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)


    # # 現在の日付を取得してフォーマット
    # current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # # ファイル名を生成
    # output_file_name = f"diff_{current_date}.txt"
    output_file_name = "diff_html.txt"

    # 差異を別ファイルに出力
    differ = difflib.Differ()
    diff = differ.compare(html_data_file.splitlines(), html_data_file_2.splitlines())

    output_file_path = os.path.join(output_dir, output_file_name)

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

    # HTMLファイルを読み込む
    with open(before_file_path, 'r') as file:
        before_html = file.read()

    with open(after_file_path, 'r') as file:
        after_html = file.read()

    return save_diff_html_data(before_html, after_html)
