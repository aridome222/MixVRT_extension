from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess



def apply_style_to_changed_elements(before_soup, after_soup):
    # タイトル（h1タグ）の変更を検出
    before_title = before_soup.find('h1')
    after_title = after_soup.find('h1')
    if before_title.text != after_title.text:
        before_title['style'] = 'border: 2px solid red;'
        after_title['style'] = 'border: 2px solid green;'

    # 新しく追加された要素（divタグのclass 'css-image'）の検出
    after_new_div = after_soup.find('div', {'class': 'css-image'})
    if after_new_div and not before_soup.find('div', {'class': 'css-image'}):
        after_new_div['style'] = 'border: 2px solid green;'

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


# 変更された要素にスタイルを適用
apply_style_to_changed_elements(before_soup, after_soup)

before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# 変更されたHTMLをファイルに書き出す
with open(before_modified_file_path, 'w') as file:
    file.write(str(before_soup))

with open(after_modified_file_path, 'w') as file:
    file.write(str(after_soup))
