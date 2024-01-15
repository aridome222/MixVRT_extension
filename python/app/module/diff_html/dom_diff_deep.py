from lxml import html

# 変更前と変更後のHTMLを定義
original_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single Content Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
        }

        .container {
            height: 300px auto;
            width: 100%;
            margin: 10px auto;
            overflow: hidden;
        }

        .main-content {
            height: 330px;
            background-color: #fff;
            padding: 5px;
            box-sizing: border-box;
        }

        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
            clear: both;
        }
    </style>
</head>

<body>
    <header>
        <h1>Single Content Web Page</h1>
    </header>
    <div class="container">
        <div class="main-content">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                deserunt mollit anim id est laborum.</p>
            <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam
                rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
                explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora
                incidunt ut labore et dolore magnam aliquam quaerat voluptatem.</p>
        </div>
    </div>
    <footer>
        <p>Footer Content</p>
    </footer>
</body>

</html>
"""

modified_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single Content Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
        }

        .container {
            height: 300px auto;
            width: 100%;
            margin: 10px auto;
            overflow: hidden;
        }

        .main-content {
            height: 330px;
            background-color: #fff;
            padding: 5px;
            box-sizing: border-box;
        }

        .main-content img {
            width: 100%;
            height: auto;
        }

        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
            clear: both;
        }
    </style>
</head>

<body>
    <header>
        <h1>Single Content Web Page</h1>
    </header>
    <div class="container">
        <div class="main-content">
            <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam
                rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
                explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
                consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
                dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora
                incidunt ut labore et dolore magnam aliquam quaerat voluptatem.</p>
            <img src="https://via.placeholder.com/1200x260" alt="Placeholder Image">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                deserunt mollit anim id est laborum.</p>
        </div>
    </div>
    <footer>
        <p>Footer Content</p>
    </footer>
</body>

</html>
"""

from lxml import html

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

# HTMLを解析してDOMツリーを作成
original_tree = html.fromstring(original_html)
modified_tree = html.fromstring(modified_html)

# body要素内での変更を比較
changes = compare_elements(original_tree, modified_tree)

# 変更があった要素を表示
for orig, modif in changes:
    orig_html = html.tostring(orig, pretty_print=True).decode() if orig is not None else "Not present in original"
    modif_html = html.tostring(modif, pretty_print=True).decode() if modif is not None else "Not present in modified"
    print(f"Original: {orig_html}")
    print(f"Modified: {modif_html}")
    print("\n")

