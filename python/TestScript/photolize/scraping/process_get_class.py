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

def apply_style_to_changes(diff_file_path):
    # テキストファイルからスタイル情報を読み込む
    with open(diff_file_path, 'r') as file:
        css_text = file.read()

    # スタイル情報を格納するリスト
    style_list = []

    # スタイル情報をセレクタ単位で分割
    css_rules = css_text.split('}')

    # 各行を処理してセレクタとスタイル情報を抽出
    for rule in css_rules:
        # 行頭の+記号を探す
        if '+' in rule:
            rule = rule.strip()  # 空白を削除
            rule = rule.lstrip('+').strip()  # +記号を取り除く
            parts = rule.split('{', 1)
            if len(parts) == 2:
                selector = parts[0].strip()
                styles = parts[1].strip('}')
                style_list.append({'selector': selector, 'style': styles})

        # 結果の表示
        for item in style_list:
            print(f'セレクタ: {item["selector"]}')
            print(f'スタイル情報: {item["style"]}')
            print('---')

# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         css_text = file.read()

#     # <style> タグ内のスタイル情報を抽出
#     start_tag = '<style>'
#     end_tag = '</style>'

#     # スタイル情報を格納するリスト
#     style_list = []

#     # <style> タグ内のスタイル情報を抽出
#     start_idx = css_text.find(start_tag)
#     end_idx = css_text.find(end_tag)
#     if start_idx != -1 and end_idx != -1:
#         style_text = css_text[start_idx + len(start_tag):end_idx].strip()

#         # スタイル情報をセレクタ単位で分割
#         css_rules = style_text.split('}')

#         # 各行を処理してセレクタとスタイル情報を抽出
#         for rule in css_rules:
#             rule = rule.strip()  # 空白を削除
#             if rule:
#                 parts = rule.split('{', 1)
#                 if len(parts) == 2:
#                     selector = parts[0].strip()
#                     styles = parts[1].strip('}')
                    
#                     # セレクタがクラスを含む場合のみ追加
#                     if '.' in selector:
#                         style_list.append({'selector': selector, 'style': styles})

#     # 結果の表示
#     for item in style_list:
#         print(f'セレクタ: {item["selector"]}')
#         print(f'スタイル情報: {item["style"]}')
#         print('---')


# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         css_text = file.read()

#     # <style> タグ内のスタイル情報を抽出
#     start_tag = '<style>'
#     end_tag = '</style>'

#     # スタイル情報を格納するリスト
#     style_list = []

#     # <style> タグ内のスタイル情報を抽出
#     start_idx = css_text.find(start_tag)
#     end_idx = css_text.find(end_tag)
#     if start_idx != -1 and end_idx != -1:
#         style_text = css_text[start_idx + len(start_tag):end_idx].strip()

#         # スタイル情報をセレクタ単位で分割
#         css_rules = style_text.split('}')

        
#         # 各行を処理してセレクタとスタイル情報を抽出
#         for rule in css_rules:
#             rule = rule.strip()  # 空白を削除
#             if rule and not re.match(r'^\s*\+', rule):  # + セレクタを除外
#                 parts = rule.split('{', 1)
#                 if len(parts) == 2:
#                     selector = parts[0].strip()
#                     styles = parts[1].strip('}')
#                     style_list.append({'selector': selector, 'style': styles})

#     # 結果の表示
#     for item in style_list:
#         print(f'セレクタ: {item["selector"]}')
#         print(f'スタイル情報: {item["style"]}')
#         print('---')


# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         css_text = file.read()

#     # スタイル情報をクラス単位で分割
#     css_lines = css_text.split('}')

#     # スタイル情報を格納するリスト
#     style_list = []

#     # 各行を処理してクラス情報を抽出
#     for line in css_lines:
#         line = line.strip()  # 空白を削除
#         if line.startswith('.'):
#             class_name = line.split('{')[0].strip()
#             style_rules = line.split('{')[1].strip('}')
#             style_list.append({'class': class_name, 'style': style_rules})

#     # 結果の表示
#     for item in style_list:
#         print(f'クラス名: {item["class"]}')
#         print(f'スタイル情報: {item["style"]}')
#         print('---')

    # content_list = []
    # flag_del = False

    # # 変更されたタグを特定し、スタイルを適用
    # for line in diff_text:
    #     if line.startswith('- '):
    #         content = line[2:].strip()
    #         if content[0] == ".":
    #             content_list = content
    #             # flag_del = True
    #             continue
    #         for elem in before_soup.find_all(True, string=lambda text: text and content in text):
    #             elem['style'] = 'border: 2px solid red;'  # 削除された部分に赤枠を適用
    #     elif line.startswith('+ '):
    #         content = line[2:].strip()
    #         for elem in after_soup.find_all(True, string=lambda text: text and content in text):
    #             elem['style'] = 'border: 2px solid green;'  # 追加された部分に緑枠を適用

    # return str(before_soup), str(after_soup)

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

apply_style_to_changes(diff_file_path)


# before_modified_html, after_modified_html = apply_style_to_changes(before_html, after_html)

# before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
# after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# # print(after_modified_html)

# # 変更されたHTMLをファイルに書き出す
# with open(before_modified_file_path, 'w') as file:
#     file.write(before_modified_html)

# with open(after_modified_file_path, 'w') as file:
#     file.write(after_modified_html)
