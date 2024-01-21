from bs4 import BeautifulSoup
import difflib
import os
import subprocess


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

# テキストコンテンツの比較
before_text = before_soup.get_text()
after_text = after_soup.get_text()

# difflibを使用して差分を取得
diff = difflib.ndiff(before_text.splitlines(), after_text.splitlines())

diff_file_path = os.path.join(output_dir, "diff.txt")

# diff ジェネレータから全てのアイテムを取り出して文字列に変換
diff_text = '\n'.join(diff)

with open(diff_file_path, 'w') as file:
    file.write(diff_text)

# ここで差分を解析して、変更された部分を特定する
# difflibを使用して変更点を特定
diff_list = list(difflib.ndiff(before_text.splitlines(), after_text.splitlines()))

print(diff_list)

# 変更された要素に対してCSSクラスを追加する
# 例：変更された要素にスタイルを適用する
for element in before_soup.find_all(string=True):
    if element in diff_list:
        element.wrap(before_soup.new_tag("span", style="border: 2px solid green;"))

for element in after_soup.find_all(string=True):
    if element in diff_list:
        element.wrap(after_soup.new_tag("span", style="border: 2px solid red;"))

before_modified_file_path = os.path.join(output_dir, 'before_modified.html')
after_modified_file_path = os.path.join(output_dir, 'after_modified.html')

# 変更されたHTMLをファイルに書き出す
with open(before_modified_file_path, 'w') as file:
    file.write(str(before_soup))

with open(after_modified_file_path, 'w') as file:
    file.write(str(after_soup))
