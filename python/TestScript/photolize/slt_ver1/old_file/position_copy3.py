# 今のところ、これを採用
# 成功作（ただし、position_copy2と比べて背景が明るめというか元画像と同じ輝度、こちらを採用する予定）
# diff_color_img.pyをより正確に差分ごとに色分けできるようにしたもの
# 連番の色枠付き画像を生成＆対応する赤枠と緑枠を出力＆赤枠と緑枠の座標と幅と高さを出力＆配置の差異判定
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np
from datetime import datetime
import subprocess


# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    command = f"sudo chown -R aridome:aridome {output_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイル名を生成
output_file_name_A = 'base.png'
output_file_name_B = 'chg_initValue.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)
output_file_path_B = os.path.join(output_dir, output_file_name_B)

img1 = cv2.imread(output_file_path_A)
img2 = cv2.imread(output_file_path_B)

# clathを使って、コントラス強調
# clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# img1_gray = clahe.apply(img1_gray)
# img2_gray = clahe.apply(img2_gray)

# img1_gray = cv2.GaussianBlur(img1_gray, (13, 13), 0)
# img2_gray = cv2.GaussianBlur(img2_gray, (13, 13), 0)

# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_img1 = cv2.subtract(img2_gray, img1_gray)
diff_img2 = cv2.subtract(img1_gray, img2_gray)
diff = cv2.absdiff(img1_gray, img2_gray)

# 二値化
ret, diff_img1 = cv2.threshold(diff_img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# diff_img1 = cv2.GaussianBlur(diff_img1, (11, 11), 0)
ret, diff_img2 = cv2.threshold(diff_img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# diff_img2 = cv2.GaussianBlur(diff_img2, (11, 11), 0)

# カーネルを準備（オープニング用）
kernel = np.ones((2,2),np.uint8)
# オープニング（収縮→膨張）実行 ノイズ除去
result_bin1 = cv2.morphologyEx(diff_img1, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。
result_bin2 = cv2.morphologyEx(diff_img2, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。

# 二値画像をRGB形式に変換
result_bin1_rgb = cv2.cvtColor(result_bin1, cv2.COLOR_GRAY2RGB)
result_bin2_rgb = cv2.cvtColor(result_bin2, cv2.COLOR_GRAY2RGB)

### 変更前と変更後の色分け ###
# 白色の範囲を定義
lower_white = np.array([200, 200, 200])  # 下限（B、G、R）
upper_white = np.array([255, 255, 255])  # 上限（B、G、R）
# lower_white2 = np.array([254, 254, 254])  # 下限（B、G、R）
# upper_white2 = np.array([255, 255, 255])  # 上限（B、G、R）

# 白色の範囲内にあるピクセルをマスクとして取得
white_mask1 = cv2.inRange(result_bin1_rgb, lower_white, upper_white)
white_mask2 = cv2.inRange(result_bin2_rgb, lower_white, upper_white)

# 緑色を指定
green_color = (0, 255, 0)  # (B、G、R)
# 赤色を指定
red_color = (0, 0, 255)  # (B、G、R)

# ピクセルの色を変更
result_bin1_rgb[white_mask1 > 0] = red_color
result_bin2_rgb[white_mask2 > 0] = green_color

# 二値画像をRGB形式に変換し、2枚の画像を重ねる。
result_diff = cv2.add(result_bin1_rgb, result_bin2_rgb)
# result = cv2.addWeighted(img1, 0.3, result_diff, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる

### 色付きの差分のみの画像を、元の画像に重ね合わせる ###
source_image = result_diff
target_image = img1

source_hsv = cv2.cvtColor(source_image, cv2.COLOR_BGR2HSV)
target_hsv = cv2.cvtColor(target_image, cv2.COLOR_BGR2HSV)

# 赤色の範囲を定義（OpenCVではHue値が0-179の範囲で表されます）
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# 赤色の範囲に対応するマスクを作成
red_mask = cv2.inRange(source_hsv, lower_red, upper_red)

# 赤色の部分を反映
target_image[red_mask > 0] = source_image[red_mask > 0]

# 緑色の範囲を定義
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# 緑色の範囲に対応するマスクを作成
green_mask = cv2.inRange(source_hsv, lower_green, upper_green)

# 緑色の部分を反映
target_image[green_mask > 0] = source_image[green_mask > 0]

### 差異が検出されたか判定 ###
# 2値画像（result_bin）の白いピクセル（差分が存在する部分）の数をカウント
white_pixel_count = cv2.countNonZero(result_bin2)

# ある閾値以上の白いピクセルが存在する場合、差分があると判断する
threshold = 100  # 適切な閾値を選択
red_text_start = "\033[91m"
red_text_end = "\033[0m"
green_text_start = "\033[92m"
green_text_end = "\033[0m"

if white_pixel_count > threshold:
    print(f"{red_text_start}差異が検出されました{red_text_end}")
else:
    print(f"{green_text_start}異常なし{green_text_end}")

# 現在の日付を取得してフォーマット
current_date = datetime.now().strftime("%m-%d_%H-%M-%S")
# ファイル名を生成
output_file_name = f"diff_color_{current_date}.png"
# output_file_name = f"diff_{current_date}.png"

output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_color_high_png/")
# output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_high_png/")

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)
    command = f"sudo chown -R aridome:aridome {output_dir2}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# 画像を保存する
cv2.imwrite(output_file_path, target_image)

print(f"2つの画像の差異を示した画像を{output_file_path}に保存しました")
