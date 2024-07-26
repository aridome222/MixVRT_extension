import os
import subprocess
from lxml import html
from lxml import etree

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def build_tree(element):
    node = TreeNode(element.tag)
    for child in element:
        if isinstance(child.tag, str):
            node.add_child(build_tree(child))
    return node

def print_tree(node, prefix='', is_last=True, output_file=None):
    def write_to_file(text):
        print(text)
        if output_file:
            output_file.write(text + '\n')

    connector = '└── ' if is_last else '├── '
    write_to_file(prefix + connector + node.name)
    for i, child in enumerate(node.children):
        new_prefix = prefix + ('    ' if is_last else '│   ')
        print_tree(child, new_prefix, i == len(node.children) - 1, output_file=output_file)

def tree_alignment_distance(tree1, tree2):
    def tad(node1, node2, dp):
        if (node1, node2) in dp:
            return dp[(node1, node2)]
        
        if not node1.children and not node2.children:
            dp[(node1, node2)] = 0 if node1.name == node2.name else 1
            return dp[(node1, node2)]

        dp[(node1, node2)] = float('inf')
        if node1.children and node2.children:
            cost = 0 if node1.name == node2.name else 1
            dp[(node1, node2)] = min(dp[(node1, node2)], tad(node1.children[0], node2.children[0], dp) + cost)
        
        if node1.children:
            dp[(node1, node2)] = min(dp[(node1, node2)], tad(node1.children[0], node2, dp) + 1)
        
        if node2.children:
            dp[(node1, node2)] = min(dp[(node1, node2)], tad(node1, node2.children[0], dp) + 1)
        
        return dp[(node1, node2)]

    dp = {}
    return tad(tree1, tree2, dp)

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
    print_tree(build_tree(before_tree), output_file=f)

with open('after_dom_tree.txt', 'w', encoding='utf-8') as f:
    f.write("After DOM Tree:\n")
    print("\nAfter DOM Tree:")
    print_tree(build_tree(after_tree), output_file=f)

print("DOMツリーをファイルに出力しました。")

# TADを使ってDOMツリーを比較
before_apt_tree = build_tree(before_tree)
after_apt_tree = build_tree(after_tree)

edit_distance = tree_alignment_distance(before_apt_tree, after_apt_tree)

print(f"Tree Alignment Distance: {edit_distance}")

# 変更を手動で追跡するための関数
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
