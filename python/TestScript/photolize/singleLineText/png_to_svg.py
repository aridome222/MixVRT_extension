# png_to_high_pngで採用
# This code example demonstrates how to convert PNG to SVG
# 参考サイト：https://blog.aspose.com/ja/words/convert-png-to-svg-in-python/
import aspose.words as aw
import os
from datetime import datetime
import cv2

#  Create document object
doc = aw.Document()

# Create a document builder object
builder = aw.DocumentBuilder(doc)

# 入力元ディレクトリを作成
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")
# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
# ファイル名を生成
input_file_name = 'chg_embed.png'
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

output_file_name = input_file_name.split(".")[0] + '.svg'

# ファイルパスを作成
output_file_path = os.path.join(output_dir, output_file_name)

# Save image as SVG
shape.get_shape_renderer().save(output_file_path, saveOptions)

print(f"pngからsvgに変換した画像を保存しました")
