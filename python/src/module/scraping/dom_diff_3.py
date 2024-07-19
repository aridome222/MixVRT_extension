"""
@author: aridome222
作成日: 2024/07/18
更新日: 2024/07/18


処理の流れ
1. 変更前と変更後のHTMLコードを読み込む
2. 変更前と変更後のDOMツリーを生成する
3. 変更前と変更後のDOMツリーを比較する
   3.1 ルートノードから再帰的に比較し、変更があればリストに追加する
   3.2 タグ名の比較
   3.3 テキストと属性の比較
   3.4 子要素の比較
       3.4.1 片方のみにあるもの、つまり追加や削除といった変更があった要素のXPathをリストに追加
       3.4.2 両方にある場合、つまり編集または変更なしまたは意図しない変更の可能性がある要素を再帰的に比較
4. 変更があった要素のXPathを表示（最終的には、変更があった要素を枠で囲む処理を加える）

"""

import os
import subprocess
from lxml import html
from lxml import etree


def get_full_xpath(element):
    """特定の要素の完全なXPathを取得する"""
    # XPathの各部分を格納するリスト
    parts = []
    # 要素が空でない限り、ループし続ける
    while element is not None:
        # 親要素を取得する
        parent = element.getparent()
        # 同じタグ名の兄弟要素のリストを取得
        siblings = parent.findall(element.tag) if parent is not None else [element]
        if len(siblings) > 1:
            # 兄弟要素が複数存在する場合、インデックスを追加
            count = siblings.index(element) + 1
            parts.append(f"{element.tag}[{count}]")
        else:
            # 兄弟要素が1つしか存在しない場合、インデックスを省略
            parts.append(element.tag)
        # 現在の要素を親要素に設定
        element = parent
    # parts リストを逆順にしてスラッシュで結合し、ルートからの完全なXPathを構築
    return '/' + '/'.join(reversed(parts))


def compare_elements(bf_elem, af_elem, ignore_order=False):
    """変更前と変更後の要素を比較して、実質的な変更があった要素のXpathのリストを返す"""
    # 実質的な変更があった要素のXPathを格納するリスト
    changes = []

    ### 変更前と変更後の親要素同士の比較 ###
    # タグ名の比較
    if bf_elem.tag != af_elem.tag:
        changes.append((get_full_xpath(bf_elem), get_full_xpath(af_elem))) # 異なる場合、リストに追加
    # テキストと属性の比較
    elif (bf_elem.text or '').strip() != (af_elem.text or '').strip() or bf_elem.attrib != af_elem.attrib:
        changes.append((get_full_xpath(bf_elem), get_full_xpath(af_elem))) # 異なる場合、リストに追加

    # 子要素リストを取得
    bf_children = list(bf_elem)
    af_children = list(af_elem)

    # # 要素の移動を変更として認めないために、タグ名、テキスト、属性で子要素をソートし、子要素の順番を無視する
    # if ignore_order:
    #     bf_children.sort(key=lambda x: (x.tag, (x.text or '').strip(), sorted(x.attrib.items())))
    #     af_children.sort(key=lambda x: (x.tag, (x.text or '').strip(), sorted(x.attrib.items())))

    # 変更前と変更後の子要素リストの長さのうち、長いほうを採用
    max_len = max(len(bf_children), len(af_children))
    ## 変更前と変更後の子要素同士の比較を子要素の数だけ行う ##
    for i in range(max_len):
        # 
        if i >= len(bf_children):
            changes.append((None, get_full_xpath(af_children[i])))
        elif i >= len(af_children):
            changes.append((get_full_xpath(bf_children[i]), None))
        else:
            changes.extend(compare_elements(bf_children[i], af_children[i], ignore_order))

    return changes


# 変更があった要素のXPathと変更内容を日本語で表示する関数
def describe_changes(orig_path, modif_path):
    if orig_path:
        return f"削除された要素のXPath: {orig_path}"
    elif modif_path:
        return f"追加された要素のXPath: {modif_path}"


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
before_tree = html.fromstring(before_html)
after_tree = html.fromstring(after_html)

# body要素内での変更を比較
changes = compare_elements(before_tree, after_tree, ignore_order=True)

# 変更があった要素の完全なXPathを表示
for change in changes:
    before_path, after_path = change
    print(describe_changes(before_path, after_path))
    print("\n")
