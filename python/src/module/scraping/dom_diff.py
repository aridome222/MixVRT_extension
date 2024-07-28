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

# def compare_dom(bf_elem, af_elem):
#     """二つの要素を比較して、実質的な変更があった要素のXpathのリストを返す"""
#     changes = []
#     if bf_elem.tag != af_elem.tag:
#         changes.append((get_full_xpath(bf_elem), get_full_xpath(af_elem)))
#     elif (bf_elem.text or '').strip() != (af_elem.text or '').strip() or bf_elem.attrib != af_elem.attrib:
#         changes.append((get_full_xpath(bf_elem), get_full_xpath(af_elem)))

#     children1 = list(bf_elem)
#     children2 = list(af_elem)
#     max_len = max(len(children1), len(children2))
#     for i in range(max_len):
#         if i >= len(children1):
#             changes.append((None, get_full_xpath(children2[i])))
#         elif i >= len(children2):
#             changes.append((get_full_xpath(children1[i]), None))
#         else:
#             changes.extend(compare_dom(children1[i], children2[i]))

#     return changes

def compare_elements(bf_elem, af_elem):
    # 3. 変更前の子要素と一致する変更後の子要素を見つける
    # 4. 見つけたら、一致した要素のペアを、一致リストに格納
    # 5. 見つからなかったら、変更前または変更後の不一致リストに格納
    pass


def compare_dom(bf_elem, af_elem, path=''):
    """ 二つの要素を比較して、変更があった要素のXpathのリストを返す """
    # 根ノードをスタートとして、再帰的に比較する
    # 0. htmlタグは必ず等しいとする
    # 1. 親要素の1つ下の階層にあるタグを見る
    # 2. 変更前の子要素と変更後の子要素を比較する
    # 3. 変更前の子要素と一致する変更後の子要素を見つける
    # 4. 見つけたら、一致した要素のペアを、一致リストに格納
    # 5. 見つからなかったら、変更前または変更後の不一致リストに格納
    # 6. 一致リストの要素ペアの子要素同士を比較するために、再帰的に自分を呼び出す
    # 7. 葉ノードに到達して比較ができなくなるか、一致リストに要素が無ければ、処理を終了する


    full_path1 = get_full_xpath(bf_elem)
    full_path2 = get_full_xpath(af_elem)
    
    changed = []

    # 1. 親要素の1つ下の階層にあるタグを見る
    for bf_chlid in bf_elem:
        for af_child in af_elem:
            ok_pairs = []
            # 2. 変更前の子要素と変更後の子要素を比較する
            ok_pairs = compare_elements(bf_chlid, af_child)
            # 6. 一致リストの要素ペアの子要素同士を比較するために、再帰的に自身を呼び出す
            for bf_elem, af_elem in ok_pairs:
                compare_dom(bf_elem, af_elem)

    # # タグ名が異なる場合、変更リストに追加
    # if bf_elem.tag != af_elem.tag:
    #     changed.append((get_full_xpath(bf_elem), get_full_xpath(af_elem)))
    
    # # 要素のテキスト、または属性が異なる場合、変更リストに追加     
    # if (bf_elem.text or '').strip() != (af_elem.text or '').strip() or bf_elem.attrib != af_elem.attrib:
    #     changed.append((full_path1, full_path2))

    # # 変更前の子要素数 > 変更後の子要素数である場合（つまり、削除が起きた場合）
    # if len(bf_elem) > len(af_elem):
    #     pass
    #     # for child1 in bf_elem:
    #     #     for child2 in af_elem:
    #     #         compare_dom(child1, child2)
    # # 変更前の子要素数 < 変更後の子要素数である場合（つまり、追加が起きた場合）
    # elif len(bf_elem) < len(af_elem):
    #     pass
    #     # for child1 in bf_elem:
    #     #     for child2 in af_elem:
    #     #         compare_dom(child1, child2)
    #     # changed.extend([(get_full_xpath(child), None) for child in bf_elem])
    #     # changed.extend([(None, get_full_xpath(child)) for child in af_elem])
    # else:
    #     # 変更前の子要素数 == 変更後の子要素数である場合
    #     for child1, child2 in zip(bf_elem, af_elem):
    #         changed.extend(compare_dom(child1, child2))

    return changed

# 変更があった要素のXPathと変更内容を日本語で表示する関数
def describe_changes(orig_path, modif_path):
    if orig_path and modif_path:
        return f"変更されたXPath: 元のXPath: {orig_path}, 変更後のXPath: {modif_path}"
    elif orig_path:
        return f"削除された要素のXPath: {orig_path}"
    elif modif_path:
        return f"追加された要素のXPath: {modif_path}"



""" メイン処理 """
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

def print_dom_tree(element, prefix='', is_last=True, output_file=None):
    # ノードをファイルに書き込む関数
    def write_to_file(text):
        print(text)  # ターミナルに出力
        if output_file:
            output_file.write(text + '\n')
        else:
            print(text)

    # 現在のノードのタグを表示
    connector = '└── ' if is_last else '├── '
    write_to_file(prefix + connector + element.tag)
    # 子要素のリストを取得
    children = [e for e in element if isinstance(e.tag, str)]
    # 子要素に対して再帰的に呼び出す
    for i, child in enumerate(children):
        new_prefix = prefix + ('    ' if is_last else '│   ')
        print_dom_tree(child, new_prefix, i == len(children) - 1, output_file=output_file)


# ファイルに出力するための準備
with open('before_dom_tree.txt', 'w', encoding='utf-8') as f:
    f.write("Before DOM Tree:\n")
    print("Before DOM Tree:")  # ターミナルに出力
    print_dom_tree(before_tree, output_file=f) # fはopen()で開いたファイルが入る

with open('after_dom_tree.txt', 'w', encoding='utf-8') as f:
    f.write("After DOM Tree:\n")
    print("\nAfter DOM Tree:")  # ターミナルに出力
    print_dom_tree(after_tree, output_file=f)

print("DOMツリーをファイルに出力しました。")

# body要素内での変更を比較
changes = compare_dom(before_tree, after_tree)

# 変更があった要素の完全なXPathを表示
for change in changes:
    before_path, after_path = change
    print(describe_changes(before_path, after_path))
    print("\n")
