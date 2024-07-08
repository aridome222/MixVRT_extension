import os
from lxml import html
from lxml import etree

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

# HTMLを解析してDOMツリーを作成
original_tree = html.fromstring(original_html)
modified_tree = html.fromstring(modified_html)

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

def compare_elements(elem1, elem2):
    """二つの要素を比較して、実質的な変更があった要素のXpathのリストを返す"""
    changes = []
    if elem1.tag != elem2.tag:
        changes.append((get_full_xpath(elem1), get_full_xpath(elem2)))
    elif (elem1.text or '').strip() != (elem2.text or '').strip() or elem1.attrib != elem2.attrib:
        changes.append((get_full_xpath(elem1), get_full_xpath(elem2)))

    children1 = list(elem1)
    children2 = list(elem2)
    max_len = max(len(children1), len(children2))
    for i in range(max_len):
        if i >= len(children1):
            changes.append((None, get_full_xpath(children2[i])))
        elif i >= len(children2):
            changes.append((get_full_xpath(children1[i]), None))
        else:
            changes.extend(compare_elements(children1[i], children2[i]))

    return changes

# 変更があった要素のXPathと変更内容を日本語で表示する関数
def describe_changes(orig_path, modif_path):
    if orig_path and modif_path:
        return f"変更されたXPath: 元のXPath: {orig_path}, 変更後のXPath: {modif_path}"
    elif orig_path:
        return f"削除された要素のXPath: {orig_path}"
    elif modif_path:
        return f"追加された要素のXPath: {modif_path}"

# body要素内での変更を比較
changes = compare_elements(original_tree, modified_tree)

# 変更があった要素の完全なXPathを表示
for change in changes:
    original_path, modified_path = change
    print(describe_changes(original_path, modified_path))
    print("\n")


# 要素を取得
element = tree.xpath(modified_path)

# 要素が存在する場合、その内容を変更する
if element:
    element[0].text = "新しい内容に変更されました。"

# 変更されたHTMLを文字列として出力
modified_html = etree.tostring(tree, pretty_print=True, encoding="unicode")
print(modified_html)