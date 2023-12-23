from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess



# 差分を取得する関数
def get_differences(before_text, after_text):
    diff = list(difflib.ndiff(before_text.splitlines(), after_text.splitlines()))
    return [line for line in diff if line.startswith('+ ') or line.startswith('- ')]

# 変更された行に対応する要素にスタイルを適用
def apply_styles_to_diffs(soup, diffs):
    for diff in diffs:
        for elem in soup.find_all(string=diff[2:].strip()):
            parent = elem.parent
            if isinstance(parent, Tag):
                if diff.startswith('+ '):
                    parent['style'] = 'border: 2px solid green;'
                elif diff.startswith('- '):
                    parent['style'] = 'border: 2px solid red;'

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

# BeautifulSoupを使用してHTMLを解析
before_soup = BeautifulSoup(before_html, 'html.parser')
after_soup = BeautifulSoup(after_html, 'html.parser')

# 差分の取得
before_diffs = get_differences(before_html, after_html)
after_diffs = get_differences(after_html, before_html)

# 変更点にスタイルを適用
apply_styles_to_diffs(before_soup, before_diffs)
apply_styles_to_diffs(after_soup, after_diffs)

before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# 変更されたHTMLをファイルに書き出す
with open(before_modified_file_path, 'w') as file:
    file.write(str(before_soup))

with open(after_modified_file_path, 'w') as file:
    file.write(str(after_soup))
