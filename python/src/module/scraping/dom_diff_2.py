import os
import subprocess
from lxml import html
from lxml import etree


def get_full_xpath(element):
    """特定の要素の完全なXPathを取得する"""
    parts = []
    while element is not None and element.tag != 'html':
        parent = element.getparent()
        siblings = parent.findall(element.tag) if parent is not None else [element]
        count = siblings.index(element) + 1
        parts.append(f"{element.tag}[{count}]")
        element = parent
    return '/' + '/'.join(reversed(parts))


def compare_elements(elem1, elem2, ignore_order=False):
    """二つの要素を比較して、実質的な変更があった要素のXpathのリストを返す"""
    changes = []
    if elem1.tag != elem2.tag:
        changes.append((get_full_xpath(elem1), get_full_xpath(elem2)))
    elif (elem1.text or '').strip() != (elem2.text or '').strip() or elem1.attrib != elem2.attrib:
        changes.append((get_full_xpath(elem1), get_full_xpath(elem2)))

    children1 = list(elem1)
    children2 = list(elem2)

    if ignore_order:
        children1.sort(key=lambda x: (x.tag, (x.text or '').strip(), sorted(x.attrib.items())))
        children2.sort(key=lambda x: (x.tag, (x.text or '').strip(), sorted(x.attrib.items())))

    max_len = max(len(children1), len(children2))
    for i in range(max_len):
        if i >= len(children1):
            changes.append((None, get_full_xpath(children2[i])))
        elif i >= len(children2):
            changes.append((get_full_xpath(children1[i]), None))
        else:
            changes.extend(compare_elements(children1[i], children2[i], ignore_order))

    return changes


# 変更があった要素のXPathと変更内容を日本語で表示する関数
def describe_changes(orig_path, modif_path, change_type="変更"):
    if change_type == "移動":
        return f"移動したXPath: 元のXPath: {orig_path}, 移動後のXPath: {modif_path}"
    elif orig_path and modif_path:
        return f"変更したXPath: 元のXPath: {orig_path}, 変更後のXPath: {modif_path}"
    elif orig_path:
        return f"削除した要素のXPath: {orig_path}"
    elif modif_path:
        return f"追加した要素のXPath: {modif_path}"


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
changes = compare_elements(before_tree, after_tree, ignore_order=True)

# 変更があった要素の完全なXPathを表示
for change in changes:
    before_path, after_path = change
    if before_path and after_path:
        print(describe_changes(before_path, after_path, change_type="移動"))
    else:
        print(describe_changes(before_path, after_path))
    print("\n")
