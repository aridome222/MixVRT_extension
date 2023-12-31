# def apply_style_to_changes(diff_file_path):
#     # テキストファイルからスタイル情報を読み込む
#     with open(diff_file_path, 'r') as file:
#         diff_text = file.read()

#     # <style> タグ内のスタイル情報を抽出
#     start_tag = '<style>'
#     end_tag = '</style>'

#     # スタイル情報を格納するリスト
#     style_list = []

#     # <style> タグ内のスタイル情報を抽出
#     start_idx = diff_text.find(start_tag)
#     end_idx = diff_text.find(end_tag)
#     if start_idx != -1 and end_idx != -1:
#         style_text = diff_text[start_idx + len(start_tag):end_idx].strip()

#         # スタイル情報をセレクタ単位で分割
#         style_rules = style_text.split('}')
#         # 各行を処理してセレクタとスタイル情報を抽出
#         for rule in style_rules:
#             # 行頭の+記号を探す
#             if '+' in rule:
#                 rule = rule.strip()  # 空白を削除
#                 rule = rule.lstrip('+').strip()  # +記号を取り除く
#                 parts = rule.split('{', 1)
#                 if len(parts) == 2:
#                     selector = parts[0].lstrip('+').strip()
#                     styles = parts[1].strip('}').replace('+', '')
#                     style_list.append({'selector': selector, 'style': styles})

#         # 結果の表示
#         for item in style_list:
#             print(f'セレクタ: {item["selector"]}')
#             print(f'スタイル情報: {item["style"]}')
#             print('---')