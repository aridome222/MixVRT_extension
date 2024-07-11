from html.parser import HTMLParser
from difflib import Differ
from bs4 import BeautifulSoup, Tag
import difflib
import os
import subprocess
from datetime import datetime
import re
import os
import stat

class CustomHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.current_tag = ""
        self.special_tags = ['style', 'script']
        self.in_special_tag = False

    def handle_starttag(self, tag, attrs):
        if tag in self.special_tags:
            self.in_special_tag = True
            self.current_tag += '<' + tag
            for attr in attrs:
                self.current_tag += ' ' + attr[0] + '="' + attr[1] + '"'
            self.current_tag += '>'

        else:
            self.tags.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.in_special_tag and tag in self.special_tags:
            self.current_tag += '</' + tag + '>'
            self.tags.append(self.current_tag)
            self.current_tag = ""
            self.in_special_tag = False
        else:
            self.tags.append('</' + tag + '>')

    def handle_data(self, data):
        if self.in_special_tag:
            self.current_tag += data
        else:
            self.tags.append(data)

def parse_html(html):
    parser = CustomHTMLParser()
    parser.feed(html)
    return parser.tags


# 保存先ディレクトリを指定
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

before_file_name = "b1.html"
after_file_name = "a1.html"

before_file_path = os.path.join(output_dir, before_file_name)
after_file_path = os.path.join(output_dir, after_file_name)

# HTMLファイルを読み込む
with open(before_file_path, 'r') as file:
    before_html = file.read()

with open(after_file_path, 'r') as file:
    after_html = file.read()

tags1 = parse_html(before_html)
tags2 = parse_html(after_html)

differ = Differ()
diff = list(differ.compare(tags1, tags2))

# 変更点を表示
for line in diff:
    print(line)
