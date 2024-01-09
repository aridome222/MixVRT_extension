from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re
import process_get_class

### 定数の定義 ###
UNIQUE_CLASS_BEFORE_CSS = """
            .uniqueClass {
                position: relative;
                /* 親要素のその他のスタイリング */
            }

            .uniqueClass::before {
                content: '';
                /* 枠のための内容は空 */
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 3px solid rgb(255, 0, 0);
                /* 枠線のスタイル */
                z-index: 1;
                /* 必要に応じて調整 */
            }

            .uniqueClass::after {
                content: '';
                position: absolute;
                top: 5px;
                /* 上からの距離を微調整 */
                left: 5px;
                /* 左からの距離を微調整 */
                color: rgb(255, 0, 0);
                font-size: 12px;
                z-index: 1;
            }
        """

UNIQUE_CLASS_AFTER_CSS = """
            .uniqueClass {
                position: relative;
                /* 親要素のその他のスタイリング */
            }

            .uniqueClass::before {
                content: '';
                /* 枠のための内容は空 */
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 3px solid rgb(0, 255, 0);
                /* 枠線のスタイル */
                z-index: 1;
                /* 必要に応じて調整 */
            }

            .uniqueClass::after {
                content: '';
                position: absolute;
                top: 5px;
                /* 上からの距離を微調整 */
                left: 5px;
                /* 左からの距離を微調整 */
                color: rgb(0, 255, 0);
                font-size: 12px;
                z-index: 1;
            }
        """


def create_html_with_css_selectors(selectors, bf_or_af_html):
    """
    Creates HTML code with specified CSS selectors.

    :param selectors: List of CSS selectors.
    :return: HTML code as a string.
    """
    # Joining the selectors with a comma for grouped CSS rules
    grouped_selectors = ', '.join(selectors)

    if bf_or_af_html == "before":
        # Creating CSS rules
        css_selector = f"""
            {grouped_selectors} {{
                position: relative;
            }}

            {', '.join(f'{selector}::before' for selector in selectors)} {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 3px solid rgb(255, 0, 0);
                z-index: 1;
            }}

            {', '.join(f'{selector}::after' for selector in selectors)} {{
                content: '';
                position: absolute;
                top: 5px;
                left: 5px;
                color: rgb(255, 0, 0);
                font-size: 12px;
                z-index: 1;
            }}
        """
    elif bf_or_af_html == "after":
        # Creating CSS rules
        css_selector = f"""
            {grouped_selectors} {{
                position: relative;
            }}

            {', '.join(f'{selector}::before' for selector in selectors)} {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 3px solid rgb(0, 255, 0);
                z-index: 1;
            }}

            {', '.join(f'{selector}::after' for selector in selectors)} {{
                content: '';
                position: absolute;
                top: 5px;
                left: 5px;
                color: rgb(0, 255, 0);
                font-size: 12px;
                z-index: 1;
            }}
        """

    return css_selector


def generate_modified_html(diff_file_path):
    ### 変更前後のhtmlのbodyタグ内の変更があった要素にunique classを追加 ###
    # <body> タグ内のスタイル情報を抽出
    start_tag = '<body>'
    end_tag = '</body>'

    # 削除されたコードと変更されていないコードを格納するリスト
    modified_before_lines = []
    modified_after_lines = []
    flag_before = False
    flag_after = False

    # テキストファイル読み込み
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()

    # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
    # 削除コード＋未変更コードを含むリストを生成
    for line in lines:
        # '-'で始まる行に処理を適用
        if line.startswith('-'):
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
 
            flag_before = True
            flag_after = False
        # '+'で始まる行に処理を適用
        elif line.startswith('+'):
            line = line[1:]  # '+'を取り除く

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

            flag_before = False
            flag_after = True
        else:
            flag_before = False
            flag_after = False

        if flag_before == False and flag_after == False:
            modified_before_lines.append(line)
            modified_after_lines.append(line)
        elif flag_before == True and flag_after == False:
            modified_before_lines.append(line)
        else:
            modified_after_lines.append(line)
        

    ### unique classを変更前後のhtmlのstyleタグ内に追加 ###
    add_uniClass_bf_lines = []
    add_uniClass_af_lines = []
    for line in modified_before_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + UNIQUE_CLASS_BEFORE_CSS + line[style_tag_index:]
        add_uniClass_bf_lines.append(line)

    for line in modified_after_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + UNIQUE_CLASS_AFTER_CSS + line[style_tag_index:]
        add_uniClass_af_lines.append(line)


    ### 変更があったCSSセレクタに対し、枠を囲むclassを追加 ###
    final_bf_lines = []
    final_af_lines = []
    # 変更されたセレクタを格納するリスト
    changed_selectors = []
    # 変更されたセレクタを抽出する関数を別ファイルから呼び出し
    changed_selectors = process_get_class.apply_style_to_changes(diff_file_path)

    css_selector_bf = create_html_with_css_selectors(changed_selectors, "before")
    css_selector_af = create_html_with_css_selectors(changed_selectors, "after")
    for line in add_uniClass_bf_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + css_selector_bf + line[style_tag_index:]
        final_bf_lines.append(line)

    for line in add_uniClass_af_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + css_selector_af + line[style_tag_index:]
        final_af_lines.append(line)


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
    modified_before_file_path = os.path.join(output_dir, "before_modified.html")
    modified_after_file_path = os.path.join(output_dir, "after_modified.html")

    with open(modified_before_file_path, 'w') as file:
        file.writelines(final_bf_lines)
        subprocess.run(['sudo', 'chown', 'aridome:aridome', modified_before_file_path])

    with open(modified_after_file_path, 'w') as file:
        file.writelines(final_af_lines)
        subprocess.run(['sudo', 'chown', 'aridome:aridome', modified_after_file_path])


"""
main処理
"""
# 保存先ディレクトリを指定
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_diff/")

# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

diff_file_path = os.path.join(input_dir, "diff_html.txt")
# 余分な // を 1 つの / に変更する処理
if diff_file_path.startswith('//'):
    diff_file_path = '/' + diff_file_path.lstrip('/')

generate_modified_html(diff_file_path)
