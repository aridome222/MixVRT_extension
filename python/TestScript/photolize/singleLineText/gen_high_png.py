# 参考サイト：https://qiita.com/skryoooo/items/a37455bef54321a6195a
# 上記のサイトのjavascriptコードをpythonコードに書き換えた
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os
from datetime import datetime
from pdf2image import convert_from_path

# 保存先ディレクトリを作成
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg_img/")
# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
# ファイル名を生成
input_file_name = 'test.svg'
# ファイルパスを作成
input_file_path = os.path.join(input_dir, input_file_name)

# SVGファイルをPDFファイルに変換する
drawing = svg2rlg(input_file_path)
pdf_file_path = os.path.join(input_dir, "image.pdf")
renderPDF.drawToFile(drawing, pdf_file_path)

# PDFファイルをPNGファイルに変換する
pdf_images = convert_from_path(pdf_file_path, dpi=500)  # 解像度を設定

# 現在の日付を取得してフォーマット
current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
# ファイル名を生成
output_file_name = f"high_svg_{current_date}.png"

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")

# ファイルパスを作成
output_file_path = os.path.join(output_dir, output_file_name)

# 保存
pdf_images[0].save(output_file_path, "PNG")

print(f"高解像度のpng画像を{output_file_path}に保存しました")
