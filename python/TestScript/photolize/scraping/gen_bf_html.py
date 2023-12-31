from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re
import process_get_class


def create_html_with_css_selectors(selectors):
    """
    Creates HTML code with specified CSS selectors.

    :param selectors: List of CSS selectors.
    :return: HTML code as a string.
    """
    # Joining the selectors with a comma for grouped CSS rules
    grouped_selectors = ', '.join(selectors)

    # Creating CSS rules
    css = f"""
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
            border: 3px solid red;
            z-index: 1;
        }}

        {', '.join(f'{selector}::after' for selector in selectors)} {{
            content: '変更箇所です。';
            position: absolute;
            top: 5px;
            left: 5px;
            color: red;
            font-size: 12px;
            z-index: 1;
        }}
    """

    return css

# できてはいるが、他の影響を考慮していないやつ
def generate_modified_before_html(diff_file_path):
    # 変更されたセレクタを格納するリスト
    changed_selectors = []

    changed_selectors = process_get_class.apply_style_to_changes(diff_file_path)

    # <body> タグ内のスタイル情報を抽出
    start_tag = '<body>'
    end_tag = '</body>'

    # 削除されたコードと変更されていないコードを格納するリスト
    modified_lines = []

    # テキストファイル読み込み
    with open(diff_file_path, 'r') as file:
        lines = file.readlines()

    # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
    # 削除コード＋未変更コードを含むリストを生成
    for line in lines:
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
            
    css = """
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
            border: 3px solid red;
            /* 枠線のスタイル */
            z-index: 1;
            /* 必要に応じて調整 */
        }

        .uniqueClass::after {
            content: '変更箇所です。';
            position: absolute;
            top: 5px;
            /* 上からの距離を微調整 */
            left: 5px;
            /* 左からの距離を微調整 */
            color: red;
            font-size: 12px;
            z-index: 1;
        }
    """

    updated_bf_lines = []
    for line in modified_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + css + line[style_tag_index:]
        updated_bf_lines.append(line)

    final_bf_lines = []
    css_selector = create_html_with_css_selectors(changed_selectors)
    for line in updated_bf_lines:
        # Find the position of the </style> tag
        style_tag_index = line.find('</style>')
        if style_tag_index != -1:
            # Insert the CSS before the </style> tag
            line = line[:style_tag_index] + css_selector + line[style_tag_index:]
        final_bf_lines.append(line)


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
        file.writelines(updated_bf_lines)
        subprocess.run(['sudo', 'chown', 'aridome:aridome', modified_file_path])


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
