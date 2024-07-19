import os
import subprocess
from lxml import html
from lxml import etree

def get_full_xpath(element):
    """ 特定の要素の完全なXPathを取得する """
    parts = []
    while element is not None and element.tag != 'html':
        parent = element.getparent()
        siblings = parent.findall(element.tag) if parent is not None else [element]
        count = siblings.index(element) + 1
        parts.append(f"{element.tag}[{count}]")
        element = parent
    return '/' + '/'.join(reversed(parts))

def compare_elements(elem1, elem2):
    """ 二つの要素を比較して、body要素内で変更があった要素のリストを返す """
    if elem1.tag != elem2.tag:
        return [(elem1, elem2)]
    
    changed = []
    # テキストの変更があった場合、変更リストに追加
    if elem1.text != elem2.text:
        changed.append((elem1, elem2))

    # 子要素の数が異なる場合、変更リストに追加
    if len(elem1) != len(elem2):
        changed.extend([(child, None) for child in elem1])
        changed.extend([(None, child) for child in elem2])
    else:
        # 子要素の数が同じ場合、それぞれ比較
        for child1, child2 in zip(elem1, elem2):
            changed.extend(compare_elements(child1, child2))

    return changed

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

# HTMLを解析してDOMツリーを作成
before_tree = html.fromstring(before_html)
after_tree = html.fromstring(after_html)

# body要素内での変更を比較
changes = compare_elements(before_tree, after_tree)

# 変更があった要素を表示
for orig, modif in changes:
    orig_html = html.tostring(orig, pretty_print=True).decode() if orig is not None else "Not present in before"
    modif_html = html.tostring(modif, pretty_print=True).decode() if modif is not None else "Not present in after"
    print(f"before: {orig_html}")
    print(f"after: {modif_html}")
    print("\n")

