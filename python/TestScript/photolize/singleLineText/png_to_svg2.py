# 不採用
# 参考サイト：https://chayarokurokuro.hatenablog.com/entry/2021/11/22/104748
import base64 # 標準ライブラリ
import svgwrite
import os
from datetime import datetime
import cv2

# 変換前画像ファイルパス
# 保存先ディレクトリを作成
input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")
# フォルダが存在しない場合は作成
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
# ファイル名を生成
input_file_name = 'test02.png'
# ファイルパスを作成
input_file_path = os.path.join(input_dir, input_file_name)

# 変換後SVGファイルパス
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg_img/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイルパスを作成
path = os.path.join(output_dir, input_file_name)
# .pngから.svgに修正
output_file_path = path.split(".")[0] + '.svg'


# 変換前画像ファイルを開く
with open(input_file_path, "rb") as f:
    img = base64.b64encode(f.read())

# 変換後ファイルを書き込む準備
dwg = svgwrite.Drawing(output_file_path)

# 保存画像のサイズ等指定と書き込み（サイズ指定が面倒）
dwg.add(dwg.image('data:image/png;base64,' + img.decode("ascii"), 
                  size=(627, 390)
                 )
        )

# ファイル保存
dwg.save()

print(f"pngからsvgに変換した画像を保存しました")