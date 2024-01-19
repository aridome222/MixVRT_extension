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
import pytesseract              # tesseract の python 用ライブラリ
from PIL import Image           # 画像処理ライブラリ

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def png_to_high_png(img_path):
    img = Image.open(img_path)
 
    # 画像のリサイズ（画像を 4 倍の大きさに変更）
    img_resize = ResizeImage(img, 2)

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

    img_resize.save(output_file_path)

    print(f"高解像度のpng画像を{output_file_path}に保存しました")

    return output_file_path


# 画像のリサイズ関数
def ResizeImage(img, magnification):
    ImgWidth = img.width * magnification
    ImgHeight = img.height * magnification
    img_resize = img.resize((int(ImgWidth), int(ImgHeight)), Image.LANCZOS)
    return img_resize