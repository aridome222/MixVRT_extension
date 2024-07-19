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

def compare_elements(elem1, elem2, path=''):
    """ 二つの要素を比較して、変更があった要素のXpathのリストを返す """
    full_path1 = get_full_xpath(elem1)
    full_path2 = get_full_xpath(elem2)

    if elem1.tag != elem2.tag:
        return [(full_path1, full_path2)]
    
    changed = []
    # テキストの変更があった場合、変更リストに追加
    if elem1.text != elem2.text:
        changed.append((full_path1, full_path2))

    # 子要素の数が異なる場合、変更リストに追加
    if len(elem1) != len(elem2):
        changed.extend([(get_full_xpath(child), None) for child in elem1])
        changed.extend([(None, get_full_xpath(child)) for child in elem2])
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

# 変更があった要素の完全なXPathを表示
for orig_path, modif_path in changes:
    print(f"before XPath: {orig_path if orig_path else 'Not present in before'}")
    print(f"after XPath: {modif_path if modif_path else 'Not present in after'}")
    print("\n")