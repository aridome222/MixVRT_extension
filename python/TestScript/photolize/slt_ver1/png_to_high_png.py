# png to high png
# 参考サイト：https://blog.aspose.com/ja/words/convert-png-to-svg-in-python/
# 参考サイト：https://qiita.com/skryoooo/items/a37455bef54321a6195a
import os
from datetime import datetime
import cv2
import aspose.words as aw
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdf2image import convert_from_path
import subprocess


#  Create document object
doc = aw.Document()

# Create a document builder object
builder = aw.DocumentBuilder(doc)

# 入力元ディレクトリを作成
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")
# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    command = f"sudo chown -R aridome:aridome {input_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイル名を生成
input_file_name = 'before.png'
# ファイルパスを作成
input_file_path = os.path.join(input_dir, input_file_name)

# Load and insert PNG image
shape = builder.insert_image(input_file_path)

# Specify image save format as SVG
saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

# # 現在の日付を取得してフォーマット
# current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
# # ファイル名を生成
# output_file_name = f"test_{current_date}.png"
# output_file_name = f"diff_view2.png"

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg_img/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

output_file_name = input_file_name.split(".")[0] + '.svg'

# ファイルパスを作成
output_file_path = os.path.join(output_dir, output_file_name)

# Save image as SVG
shape.get_shape_renderer().save(output_file_path, saveOptions)

print(f"pngからsvgに変換した画像を保存しました")

# SVGファイルをPDFファイルに変換する
drawing = svg2rlg(output_file_path)
pdf_file_path = os.path.join(output_dir, "image.pdf")
renderPDF.drawToFile(drawing, pdf_file_path)

# PDFファイルをPNGファイルに変換する
pdf_images = convert_from_path(pdf_file_path, dpi=300)  # 解像度を設定

# PDFファイルを削除する
if os.path.exists(pdf_file_path):
    os.remove(pdf_file_path)

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイルパスを作成
output_file_path = os.path.join(output_dir, input_file_name)

# 保存
pdf_images[0].save(output_file_path, "PNG")

print(f"高解像度のpng画像を{output_file_path}に保存しました")
