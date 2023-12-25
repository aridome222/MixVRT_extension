from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


# def generate_modified_before_html(diff_file_path):
#     start_tag = '<body>'
#     end_tag = '</body>'

#     modified_lines = []

#     with open(diff_file_path, 'r') as file:
#         lines = file.readlines()

#     inside_body_tag = False  # <body> タグ内かどうかを追跡するフラグ
#     for line in lines:
#         # <body> タグを検出
#         if start_tag in line:
#             inside_body_tag = True

#         # <body> タグ内の場合のみ処理を適用
#         if inside_body_tag:
#             if line.startswith('+'):
#                 continue
#             elif line.startswith('-'):
#                 line = line[1:]  # '-'を取り除く

#                 if '<' in line and '>' in line:
#                     if "class=" in line:
#                         class_index = line.find('class=')
#                         class_end_index = line.find('"', class_index + 7)
#                         line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
#                     else:
#                         tag_end_index = line.find('>')
#                         line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]

#         modified_lines.append(line)

#         # </body> タグを検出
#         if end_tag in line:
#             inside_body_tag = False


def generate_modified_before_html(diff_file_path):
    # <body> タグ内のスタイル情報を抽出
    start_body_tag = '<body>'
    end_body_tag = '</body>'
    inside_body_tag = False  # <body> タグ内かどうかを追跡するフラグ

    # 削除されたコードと変更されていないコードを格納するリスト
    modified_lines = []

    # テキストファイル読み込み
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()

    # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
    # 削除コード＋未変更コードを含むリストを生成
    for line in lines:
        if body開始タグであれば:
            body_flag = True
            pass

        if style開始タグであれば:

        if body_flag == True:
            # body内における処理
            pass
        else style_flag == True:






        # '+'で始まる行をスキップ
        if line.startswith('+'):
            continue
        # '-'で始まる行に処理を適用
        elif line.startswith('-'):
            line = line[1:]  # '-'を取り除く

            # 行中にタグが存在する場合
            if '<' in line and '>' in line:
                # タグ内にclass属性が既にあれば、class=""の中の末尾に事前定義classを挿入
                if "class=" in line:
                    class_index = line.find('class=')
                    class_end_index = line.find('"', class_index + 7)
                    line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
                # タグ内にclass属性が無ければ、終了タグ直前に事前定義classを挿入
                else:
                    tag_end_index = line.find('>')
                    line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]

        # 加工した削除コード or 未変更のコードをリストに追加
        modified_lines.append(line)


# できてはいるが、他の影響を考慮していないやつ
# def generate_modified_before_html(diff_file_path):
#     # <body> タグ内のスタイル情報を抽出
#     start_tag = '<body>'
#     end_tag = '</body>'

#     # 削除されたコードと変更されていないコードを格納するリスト
#     modified_lines = []

#     # テキストファイル読み込み
#     with open(diff_file_path, 'r') as file:
#         lines = file.readlines()

#     # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
#     # 削除コード＋未変更コードを含むリストを生成
#     for line in lines:
#         # '+'で始まる行をスキップ
#         if line.startswith('+'):
#             continue
#         # '-'で始まる行に処理を適用
#         elif line.startswith('-'):
#             line = line[1:]  # '-'を取り除く

#             # 行中にタグが存在する場合
#             if '<' in line and '>' in line:
#                 # タグ内にclass属性が既にあれば、class=""の中の末尾に事前定義classを挿入
#                 if "class=" in line:
#                     class_index = line.find('class=')
#                     class_end_index = line.find('"', class_index + 7)
#                     line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
#                 # タグ内にclass属性が無ければ、終了タグ直前に事前定義classを挿入
#                 else:
#                     tag_end_index = line.find('>')
#                     line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]

#         # 加工した削除コード or 未変更のコードをリストに追加
#         modified_lines.append(line)

            
# .uniqueClass {
#             position: relative;
#             /* 親要素のその他のスタイリング */
#         }

#         .uniqueClass::before {
#             content: '';
#             /* 枠のための内容は空 */
#             position: absolute;
#             top: 0;
#             left: 0;
#             right: 0;
#             bottom: 0;
#             border: 3px solid red;
#             /* 枠線のスタイル */
#             z-index: 1;
#             /* 必要に応じて調整 */
#         }

#         .uniqueClass::after {
#             content: '変更箇所です。';
#             position: absolute;
#             top: 5px;
#             /* 上からの距離を微調整 */
#             left: 5px;
#             /* 左からの距離を微調整 */
#             color: red;
#             font-size: 12px;
#             z-index: 1;
#         }

    # 保存先ディレクトリを指定
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # 加工したHTMLを保存（拡張子を.htmlにする）
    modified_file_path = os.path.join(output_dir, "before_modified.html")

    with open(modified_file_path, 'w') as file:
        file.writelines(modified_lines)


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
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

diff_file_path = os.path.join(input_dir, "diff_html.txt")
generate_modified_before_html(diff_file_path)


# # 余分な // を 1 つの / に変更する処理
# if diff_file_path.startswith('//'):
#     diff_file_path = '/' + diff_file_path.lstrip('/')

# apply_style_to_changes(diff_file_path)


# before_modified_html, after_modified_html = apply_style_to_changes(before_html, after_html)

# before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
# after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# # print(after_modified_html)

# # 変更されたHTMLをファイルに書き出す
# with open(before_modified_file_path, 'w') as file:
#     file.write(before_modified_html)

# with open(after_modified_file_path, 'w') as file:
#     file.write(after_modified_html)
