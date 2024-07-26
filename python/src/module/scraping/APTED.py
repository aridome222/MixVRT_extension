import os
import subprocess
from lxml import html
from lxml import etree
from apted.apted import APTED, Config
from apted.helpers import Tree


class MyTree(Tree):
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []


def get_full_xpath(element):
    """特定の要素の完全なXPathを取得する"""
    parts = []
    while element is not None:
        parent = element.getparent()
        siblings = parent.findall(element.tag) if parent is not None else [element]
        if len(siblings) > 1:
            count = siblings.index(element) + 1
            parts.append(f"{element.tag}[{count}]")
        else:
            parts.append(element.tag)
        element = parent
    return '/' + '/'.join(reversed(parts))


def element_to_tree(element):
    """lxmlの要素をAPTのツリー構造に変換する"""
    children = [element_to_tree(child) for child in element if isinstance(child.tag, str)]
    return MyTree(element.tag, children)


def print_dom_tree(element, prefix='', is_last=True, output_file=None):
    def write_to_file(text):
        print(text)
        if output_file:
            output_file.write(text + '\n')

    connector = '└── ' if is_last else '├── '
    write_to_file(prefix + connector + element.tag)
    children = [e for e in element if isinstance(e.tag, str)]
    for i, child in enumerate(children):
        new_prefix = prefix + ('    ' if is_last else '│   ')
        print_dom_tree(child, new_prefix, i == len(children) - 1, output_file=output_file)


# メイン処理
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_data/")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    subprocess.call(command, shell=True)

before_file_name = "b1.html"
after_file_name = "a1.html"

before_file_path = os.path.join(output_dir, before_file_name)
after_file_path = os.path.join(output_dir, after_file_name)

with open(before_file_path, 'r') as file:
    before_html = file.read()

with open(after_file_path, 'r') as file:
    after_html = file.read()

before_tree = html.fromstring(before_html)
after_tree = html.fromstring(after_html)

with open('before_dom_tree.txt', 'w', encoding='utf-8') as f:
    f.write("Before DOM Tree:\n")
    print("Before DOM Tree:")
    print_dom_tree(before_tree, output_file=f)

with open('after_dom_tree.txt', 'w', encoding='utf-8') as f:
    f.write("After DOM Tree:\n")
    print("\nAfter DOM Tree:")
    print_dom_tree(after_tree, output_file=f)

print("DOMツリーをファイルに出力しました。")

# APTEDを使ってDOMツリーを比較
before_apt_tree = element_to_tree(before_tree)
after_apt_tree = element_to_tree(after_tree)

class CustomConfig(Config):
    def rename(self, node1, node2):
        return int(node1.name != node2.name)

apted = APTED(before_apt_tree, after_apt_tree, CustomConfig())
edit_distance = apted.compute_edit_distance()

print(f"Edit Distance: {edit_distance}")

# 手動で変更を追跡
def find_changes(before, after, path=""):
    changes = []
    if before.name != after.name:
        changes.append(f"Rename {path}/{before.name} to {after.name}")
    before_children = {child.name: child for child in before.children}
    after_children = {child.name: child for child in after.children}
    
    for name in before_children:
        if name not in after_children:
            changes.append(f"Delete {path}/{before_children[name].name}")
        else:
            changes.extend(find_changes(before_children[name], after_children[name], f"{path}/{name}"))
    
    for name in after_children:
        if name not in before_children:
            changes.append(f"Insert {path}/{after_children[name].name}")
    
    return changes

changes = find_changes(before_apt_tree, after_apt_tree)
for change in changes:
    print(change)
