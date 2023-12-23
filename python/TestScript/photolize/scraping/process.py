from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re

def save_diff_html_data(html_data_file, html_data_file_2):
    ### ２つのHTMLデータの差分をtxtファイルに出力する ###

    # 保存先ディレクトリを指定
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")
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
        f.write("\n".join(diff))

    print(f"2つのHTMLデータの差異を{output_file_path}に保存しました")


def split_code_into_files(input_file_path):
    # テキストファイルの読み込み
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # print(lines)

    # 変更されていないコード、削除されたコード、追加されたコードを格納するためのリスト
    unchanged_code = []
    deleted_code = []
    added_code = []

    # 行ごとに処理
    for line in lines:
        if line.startswith('- '):  # 削除されたコードの開始
            deleted_code.append(line[2:])  # 先頭の '-' を取り除いて追加
        elif line.startswith('+ '):  # 追加されたコード
            added_code.append(line[2:])  # 先頭の '+' を取り除いて追加
        else:  # 変更されていないコード
            unchanged_code.append(line)

    # 保存先ディレクトリを指定
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "split/")
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
    unchanged_file_path = os.path.join(output_dir, "unchanged_html.txt")
    del_file_path = os.path.join(output_dir, "del_html.txt")
    add_file_path = os.path.join(output_dir, "add_html.txt")

    # 変更されていないコードを保存
    with open(unchanged_file_path, 'w', encoding='utf-8') as file:
        file.writelines(unchanged_code)

    # 削除されたコードを保存
    with open(del_file_path, 'w', encoding='utf-8') as file:
        file.writelines(deleted_code)

    # 追加されたコードを保存
    with open(add_file_path, 'w', encoding='utf-8') as file:
        file.writelines(added_code)


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

save_diff_html_data(before_html, after_html)

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

split_code_into_files(diff_file_path)

# 保存先ディレクトリを指定
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "split/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

add_file_path = os.path.join(input_dir, "add_html.txt")
del_file_path = os.path.join(input_dir, "del_html.txt")
unchanged_file_path = os.path.join(input_dir, "unchanged_html.txt")



# before_modified_html, after_modified_html = apply_style_to_changes(before_html, after_html)

# before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
# after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# # print(after_modified_html)

# # 変更されたHTMLをファイルに書き出す
# with open(before_modified_file_path, 'w') as file:
#     file.write(before_modified_html)

# with open(after_modified_file_path, 'w') as file:
#     file.write(after_modified_html)
