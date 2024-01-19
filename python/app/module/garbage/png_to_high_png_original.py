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
import shutil


# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def png_to_high_png(img_path):
    #  Create document object
    doc = aw.Document()

    # Create a document builder object
    builder = aw.DocumentBuilder(doc)

    # Load and insert PNG image
    shape = builder.insert_image(img_path)

    # Specify image save format as SVG
    saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

    # # 現在の日付を取得してフォーマット
    # current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
    # # ファイル名を生成
    # output_file_name = f"test_{current_date}.png"
    # output_file_name = f"diff_view2.png"

    svg_dir = os.path.join(diff_dir, "svg_img/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(svg_dir):
        os.makedirs(svg_dir)
        command = f"sudo chown -R aridome:aridome {svg_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    svg_file_name = "image.svg"

    # ファイルパスを作成
    svg_file_path = os.path.join(svg_dir, svg_file_name)

    # Save image as SVG
    shape.get_shape_renderer().save(svg_file_path, saveOptions)

    print(f"pngからsvgに変換した画像を保存しました")

    # SVGファイルをPDFファイルに変換する
    drawing = svg2rlg(svg_file_path)
    pdf_file_path = os.path.join(svg_dir, "image.pdf")
    renderPDF.drawToFile(drawing, pdf_file_path)

    # PDFファイルをPNGファイルに変換する
    pdf_images = convert_from_path(pdf_file_path, dpi=300)  # 解像度を設定

    # svg_dirを削除する
    if os.path.exists(svg_dir):
        shutil.rmtree(svg_dir)

    output_dir = os.path.join(os.path.dirname(img_path), "high_png/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    output_file_name = os.path.basename(img_path)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir, output_file_name)

    # 保存
    pdf_images[0].save(output_file_path, "PNG")

    print(f"高解像度のpng画像を{output_file_path}に保存しました")

    return output_file_path