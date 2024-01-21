from lxml import etree, html

def extract_changed_elements(html_content, tags):
    """ HTMLコンテンツから特定のタグを含む変更された要素を抽出する """
    tree = html.fromstring(html_content)
    namespace = {'diff': 'http://namespaces.shoobx.com/diff'}
    changed_elements = []

    for tag in tags:
        # 変更されたタグを検索
        for elem in tree.xpath(f'//*[contains(@diff:insert, "") and local-name()="{tag}"]', namespaces=namespace):
            changed_elements.append(etree.tostring(elem, pretty_print=True).decode())

        # diff:insertを含むテキストノードを検索
        for elem in tree.xpath(f'//{tag}[descendant::diff:insert]', namespaces=namespace):
            changed_elements.append(etree.tostring(elem, pretty_print=True).decode())

    return changed_elements

# HTMLコンテンツ
html_content = """
<div xmlns:diff="http://namespaces.shoobx.com/diff">
    <header>
        <h1>Single Content Web Page</h1>
    </header>
    <div class="container">
        <div class="main-content">
            <img diff:insert="" alt="Placeholder Image" diff:add-attr="alt;src" src="https://via.placeholder.com/1200x260"/><diff:insert>
            </diff:insert><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla par<diff:insert>aa</diff:insert>iatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
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
</div>
"""  # ここに先ほどのHTMLを入れる

# 変更された<img>と<p>タグを抽出
changed_elements = extract_changed_elements(html_content, ['img', 'p'])

# 結果を表示
for elem in changed_elements:
    print(elem)