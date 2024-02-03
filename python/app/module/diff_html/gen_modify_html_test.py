from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re


# from module.diff_html import process_get_class


# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


### 定数の定義 ###
UNIQUE_CLASS_BEFORE_CSS = """
<style>
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
                border: 5px solid rgb(255, 0, 0);
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
</style>
        """

UNIQUE_CLASS_AFTER_CSS = """
<style>
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
                border: 5px solid rgb(0, 255, 0);
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
</style>
        """

IMAGE_WRAPPER_CLASS_BEFORE_CSS = """
<style>
            .image-wrapper {
                position: relative;
            }

            .image-wrapper::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 5px solid rgb(255, 0, 0); /* 枠線のスタイル */
                z-index: 1;
            }
</style>
        """

IMAGE_WRAPPER_CLASS_AFTER_CSS = """
<style>
            .image-wrapper {
                position: relative;
            }

            .image-wrapper::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border: 5px solid rgb(0, 255, 0); /* 枠線のスタイル */
                z-index: 1;
            }
</style>
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
        <style>
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
        </style>
        """
    elif bf_or_af_html == "after":
        # Creating CSS rules
        css_selector = f"""
        <style>
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
        </style>
        """

    return css_selector


def generate_modified_html(diff_file_path):
    ### 変更前後のhtmlのbodyタグ内の変更があった要素にunique classを追加 ###
    # <body> タグ内のスタイル情報を抽出
    start_body_tag = '<body>'
    end_body_tag = '</body>'
    inside_body_tag = False

    # 削除されたコードと変更されていないコードを格納するリスト
    modified_before_lines = []
    modified_after_lines = []
    flag_before = False
    flag_after = False

    # <img>のような空要素の変更に対してラップクラスを追加したかどうかのフラグ
    flag_wrapper = False

    # テキストファイル読み込み
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()

    # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
    # 削除コード＋未変更コードを含むリストを生成
    for line in lines:        
        # body要素の開始と終了を検出
        if start_body_tag in line:
            inside_body_tag = True
        elif end_body_tag in line:
            inside_body_tag = False


        # body要素外の行に対する処理
        if not inside_body_tag:
            if line.startswith('-'):
                modified_before_lines.append(line[1:])  # 先頭の'-'を取り除く
            elif line.startswith('+'):
                modified_after_lines.append(line[1:])  # 先頭の'+'を取り除く
            else:
                # '+'や'-'で始まらない行は両方のリストに追加
                modified_before_lines.append(line)
                modified_after_lines.append(line)
        # body要素内の行に対する処理
        else:
            # '-'または'+'で始まる行に対する処理
            if line.startswith('-') or line.startswith('+'):
                modified_line = line[1:]  # 先頭の'-'または'+'を取り除く

                # <img> タグが含まれている場合、.image-wrapper で囲む
                if '<img' in modified_line:
                    modified_line = '<div class="image-wrapper">\n' + modified_line + '</div>\n'
                    flag_wrapper = True
                else:
                    # 行中にタグが存在するかチェック
                    if '<' in line and '>' in line:
                        # タグ内にclass属性が既にあれば、class=""の中の末尾に uniqueClass を挿入
                        if "class=" in modified_line:
                            class_index = modified_line.find('class=')
                            class_end_index = modified_line.find('"', class_index + 7)
                            modified_line = modified_line[:class_end_index] + " uniqueClass" + modified_line[class_end_index:]
                        # タグ内にclass属性が無ければ、開始タグか終了タグかをチェック
                        else:
                            tag_start_index = modified_line.find('<')
                            if tag_start_index != -1:  # タグが見つかった場合のみ処理を進める
                                if modified_line[tag_start_index + 1] != '/':  # 開始タグであれば
                                    tag_end_index = modified_line.find('>')
                                    modified_line = modified_line[:tag_end_index] + ' class="uniqueClass"' + modified_line[tag_end_index:]

                # '-'で始まる行と'+'で始まる行に別々に処理を適用
                if line.startswith('-'):
                    flag_before = True
                    flag_after = False
                elif line.startswith('+'):
                    flag_before = False
                    flag_after = True
            else:
                modified_line = line
                flag_before = False
                flag_after = False

            # 変更された行を適切なリストに追加
            if flag_before == False and flag_after == False:
                modified_before_lines.append(modified_line)
                modified_after_lines.append(modified_line)
            elif flag_before == True and flag_after == False:
                modified_before_lines.append(modified_line)
            else:
                modified_after_lines.append(modified_line)
        

    ### unique classを変更前後のhtmlのstyleタグ内に追加 ###
    add_uniClass_bf_lines = []
    add_uniClass_af_lines = []
    for line in modified_before_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</head>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + UNIQUE_CLASS_BEFORE_CSS + line[style_tag_index:]
        add_uniClass_bf_lines.append(line)

    for line in modified_after_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</head>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + UNIQUE_CLASS_AFTER_CSS + line[style_tag_index:]
        add_uniClass_af_lines.append(line)


    ### 変更があったCSSセレクタに対し、枠を囲むclassを追加 ###
    final_bf_lines = []
    final_af_lines = []
    # 変更されたセレクタを格納するリスト
    changed_selectors = []

    # 正規表現パターン
    # img がセレクタに含まれるケースにマッチする
    # 例: .class img, #id img, img.class, img#id, img
    # \s*{ は任意の空白文字に続く { にマッチ
    # .*?} は非貪欲な方法で最初の } までの任意の文字にマッチ
    pattern = r'[^\s{}]*\s*img[^\s{}]*\s*{.*?}'

    # 変更されたセレクタを抽出する関数を別ファイルから呼び出し
    changed_selectors = apply_style_to_changes(diff_file_path)
    flag_changed_selectors = False
    if len(changed_selectors) > 0:
        flag_changed_selectors = True

    # マッチするセレクタを格納するリスト
    img_selectors = []
    is_exist_changed_img_selectors = False

    # リスト内の各セレクタに対してマッチングを試みる
    for selector in changed_selectors:
        if re.search(pattern, selector):
            img_selectors.append(selector)
            is_exist_changed_img_selectors = True

    css_selector_bf = create_html_with_css_selectors(changed_selectors, "before")
    css_selector_af = create_html_with_css_selectors(changed_selectors, "after")
    for line in add_uniClass_bf_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</head>')
        if style_tag_index != -1:
            if flag_changed_selectors:
                # Insert the CSS before the </style> tag
                line = line[:style_tag_index] + css_selector_bf + line[style_tag_index:]
            if is_exist_changed_img_selectors or flag_wrapper:
                line = line[:style_tag_index] + IMAGE_WRAPPER_CLASS_BEFORE_CSS + line[style_tag_index:]

        final_bf_lines.append(line)

    for line in add_uniClass_af_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</head>')
        if style_tag_index != -1:
            if flag_changed_selectors:
                # Insert the CSS before the </style> tag
                line = line[:style_tag_index] + css_selector_af + line[style_tag_index:]
            if is_exist_changed_img_selectors or flag_wrapper:
                line = line[:style_tag_index] + IMAGE_WRAPPER_CLASS_AFTER_CSS + line[style_tag_index:]

        final_af_lines.append(line)


    ### 編集したファイルの保存 ###
    create_dir_and_set_owner(os.path.join(diff_dir, "modified_html"))
    # 保存先ディレクトリを指定
    output_dir = os.path.join(diff_dir, "modified_html", "templates")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # 編集したHTMLを保存（拡張子を.htmlにする）
    modified_before_file_path = os.path.join(output_dir, "modified_testPage_bf.html")
    modified_after_file_path = os.path.join(output_dir, "modified_testPage_af.html")

    with open(modified_before_file_path, 'w') as file:
        file.writelines(final_bf_lines)
        subprocess.run(['sudo', 'chown', 'aridome:aridome', modified_before_file_path])

    with open(modified_after_file_path, 'w') as file:
        file.writelines(final_af_lines)
        subprocess.run(['sudo', 'chown', 'aridome:aridome', modified_after_file_path])

    return modified_before_file_path, modified_after_file_path

"""
main処理
"""
def main(diff_html_file_path):
    # 余分な // を 1 つの / に変更する処理
    if diff_html_file_path.startswith('//'):
        diff_html_file_path = '/' + diff_html_file_path.lstrip('/')

    return generate_modified_html(diff_html_file_path)


def apply_style_to_changes(diff_file_path):
    with open(diff_file_path, 'r') as file:
        diff_lines = file.readlines()

    changed_selectors = []
    current_selector = None

    for line in diff_lines:
        if '{' in line:
            selector = line.split('{')[0].strip().strip('+').strip('-').strip()
            if line.startswith('+') or line.startswith('-'):
                if selector not in changed_selectors:
                    changed_selectors.append(selector)
            current_selector = selector
            continue

        if '}' in line:
            current_selector = None
            continue

        if current_selector is not None and (line.startswith('+') or line.startswith('-')):
            if current_selector not in changed_selectors:
                changed_selectors.append(current_selector)

    print(f"変更があったcssセレクタ: {changed_selectors}")

    return changed_selectors