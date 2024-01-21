# # body内における+,-のみを対象とした処理を行うようにしたもの
# def generate_modified_before_html(diff_file_path):
#     start_body_tag = '<body>'
#     end_body_tag = '</body>'

#     start_style_tag = '<style>'
#     end_style_tag = '</style>'

#     modified_lines = []

#     with open(diff_file_path, 'r') as file:
#         lines = file.readlines()

#     inside_body_tag = False  # <body> タグ内かどうかを追跡するフラグ
#     inside_style_tag = False  # <style> タグ内かどうかを追跡するフラグ
#     for line in lines:
#         # <body> タグを検出
#         if start_body_tag in line:
#             inside_body_tag = True

#         # <body> タグ内の場合のみ処理を適用
#         if inside_body_tag:
#             if line.startswith('+'):
#                 continue
#             elif line.startswith('-'):
#                 line = line[1:]  # '-'を取り除く

#                 if '<' in line and '>' in line:
#                     if "class=" in line:
#                         class_index = line.find('class=')
#                         class_end_index = line.find('"', class_index + 7)
#                         line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
#                     else:
#                         tag_end_index = line.find('>')
#                         line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]

#         modified_lines.append(line)

#         # </body> タグを検出
#         if end_body_tag in line:
#             inside_body_tag = False

    


# def generate_modified_before_html(diff_file_path):
#     # <body> タグ内のスタイル情報を抽出
#     start_body_tag = '<body>'
#     end_body_tag = '</body>'
#     inside_body_tag = False  # <body> タグ内かどうかを追跡するフラグ

#     # 削除されたコードと変更されていないコードを格納するリスト
#     modified_lines = []

#     # テキストファイル読み込み
#     with open(diff_file_path, 'r') as file:
#         lines = file.readlines()

#     # ファイルの各行に対して、削除コードには事前定義したclassを追加し、
#     # 削除コード＋未変更コードを含むリストを生成
#     for line in lines:
#         if body開始タグであれば:
#             body_flag = True
#             pass

#         if style開始タグであれば:

#         if body_flag == True:
#             # body内における処理
#             pass
#         else style_flag == True:






#         # '+'で始まる行をスキップ
#         if line.startswith('+'):
#             continue
#         # '-'で始まる行に処理を適用
#         elif line.startswith('-'):
#             line = line[1:]  # '-'を取り除く

#             # 行中にタグが存在する場合
#             if '<' in line and '>' in line:
#                 # タグ内にclass属性が既にあれば、class=""の中の末尾に事前定義classを挿入
#                 if "class=" in line:
#                     class_index = line.find('class=')
#                     class_end_index = line.find('"', class_index + 7)
#                     line = line[:class_end_index] + " uniqueClass" + line[class_end_index:]
#                 # タグ内にclass属性が無ければ、終了タグ直前に事前定義classを挿入
#                 else:
#                     tag_end_index = line.find('>')
#                     line = line[:tag_end_index] + ' class="uniqueClass"' + line[tag_end_index:]

#         # 加工した削除コード or 未変更のコードをリストに追加
#         modified_lines.append(line)


# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         css_text = file.read()

#     # スタイル情報をクラス単位で分割
#     css_lines = css_text.split('}')

#     # スタイル情報を格納するリスト
#     style_list = []

#     # 各行を処理してクラス情報を抽出
#     for line in css_lines:
#         line = line.strip()  # 空白を削除
#         if line.startswith('.'):
#             class_name = line.split('{')[0].strip()
#             style_rules = line.split('{')[1].strip('}')
#             style_list.append({'class': class_name, 'style': style_rules})

#     # 結果の表示
#     for item in style_list:
#         print(f'クラス名: {item["class"]}')
#         print(f'スタイル情報: {item["style"]}')
#         print('---')

    # content_list = []
    # flag_del = False

    # # 変更されたタグを特定し、スタイルを適用
    # for line in diff_text:
    #     if line.startswith('- '):
    #         content = line[2:].strip()
    #         if content[0] == ".":
    #             content_list = content
    #             # flag_del = True
    #             continue
    #         for elem in before_soup.find_all(True, string=lambda text: text and content in text):
    #             elem['style'] = 'border: 2px solid red;'  # 削除された部分に赤枠を適用
    #     elif line.startswith('+ '):
    #         content = line[2:].strip()
    #         for elem in after_soup.find_all(True, string=lambda text: text and content in text):
    #             elem['style'] = 'border: 2px solid green;'  # 追加された部分に緑枠を適用

    # return str(before_soup), str(after_soup)