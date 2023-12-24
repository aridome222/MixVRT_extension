from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


def generate_modified_before_html(diff_file_path):
    modified_lines = []

    with open(diff_file_path, 'r') as file:
        for line in file:
            # '+'で始まる行を削除する
            if line.startswith('+'):
                continue
            # '-'で始まる行にスタイルを適用し、'-'を取り除く
            elif line.startswith('-'):
                line = line[1:]  # '-'を取り除く
                # HTMLタグを探し、クラスを追加する
                if '<' in line and '>' in line:
                    if "class=" in line:
                        # class属性の位置を見つける
                        class_index = line.find('class=')
                        # class属性の値の終わりを見つける
                        class_end_index = line.find('"', class_index + 7)
                        # 新しいクラス名を追加
                        line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
                    else:
                        # タグの終わりを見つける
                        tag_end_index = line.find('>')
                        # class属性を追加
                        line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]
                modified_lines.append(line)
            else:
                modified_lines.append(line)



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
