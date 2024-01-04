# 失敗作
# diff_color_img.pyをより正確に差分ごとに色分けできるようにしたもの
# 連番の色枠付き画像を生成＆対応する赤枠と緑枠を出力＆赤枠と緑枠の座標と幅と高さを出力＆配置の差異判定
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np

# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイル名を生成
output_file_name_A = 'bf_html2.png'
output_file_name_B = 'af_html2.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)
output_file_path_B = os.path.join(output_dir, output_file_name_B)

img1 = cv2.imread(output_file_path_A)
img2 = cv2.imread(output_file_path_B)

clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img1_gray = clahe.apply(img1_gray)
img2_gray = clahe.apply(img2_gray)

img1_gray = cv2.GaussianBlur(img1_gray, (13, 13), 0)
img2_gray = cv2.GaussianBlur(img2_gray, (13, 13), 0)

# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_img1 = cv2.subtract(img1_gray, img2_gray)
diff_img2 = cv2.subtract(img2_gray, img1_gray)

# 二値化
ret, diff_img1 = cv2.threshold(diff_img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# diff_img1 = cv2.GaussianBlur(diff_img1, (11, 11), 0)
ret, diff_img2 = cv2.threshold(diff_img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# diff_img2 = cv2.GaussianBlur(diff_img2, (11, 11), 0)

# 白色の範囲を定義
lower_white = np.array([128, 128, 128], dtype=np.uint8)  # 下限（B、G、R）
upper_white = np.array([254, 254, 254], dtype=np.uint8)  # 上限（B、G、R）

# 白色の範囲内にあるピクセルをマスクとして取得
white_mask = cv2.inRange(diff_img1, lower_white, upper_white)

# 新しい色（緑色）を指定
new_color = np.array([0, 255, 0], dtype=np.uint8)  # 新しい色（BGR形式、緑色）

# ピクセルの色を変更
diff_img1[white_mask > 0] = new_color


# 白い色を定義（BGR形式で白色を表します）
# white_color = np.array([255, 255, 255], dtype=np.uint8)

# # 画像内の白いピクセルを赤色に変更
# # ピクセルごとに白色かどうかを確認し、白色の場合は赤色に変更
# for i in range(diff_img1.shape[0]):
#     for j in range(diff_img1.shape[1]):
#         pixel = diff_img1[i, j]
#         if np.array_equal(pixel, white_color):
#             diff_img1[i, j] = [0, 0, 255]  # 赤色に変更（BGR形式）

# # ピクセルごとに白色かどうかを確認し、白色の場合は赤色に変更
# for i in range(diff_img2.shape[0]):
#     for j in range(diff_img2.shape[1]):
#         pixel = diff_img2[i, j]
#         if np.array_equal(pixel, white_color):
#             diff_img2[i, j] = [0, 255, 0]  # 赤色に変更（BGR形式）

# 二値画像をRGB形式に変換し、2枚の画像を重ねる。
img1_color = cv2.cvtColor(diff_img1, cv2.COLOR_GRAY2RGB)
result_add = cv2.addWeighted(img2, 0.3, img1_color, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる
img2_color = cv2.cvtColor(diff_img2, cv2.COLOR_GRAY2RGB)
result_add = cv2.addWeighted(result_add, 0.3, img2_color, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる


# # 赤枠に番号を割り振りながら座標を出力
# for i, (x, y, w, h) in enumerate(red_rectangles, start=1):
#     cv2.putText(img2, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
#     print(f"赤枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# # 緑枠に番号を割り振りながら座標を出力
# for i, (x, y, w, h) in enumerate(green_rectangles, start=1):
#     cv2.putText(img2, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
#     print(f"緑枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# 差分画像を保存
if output_file_name_B == "base.png":
    output_file_name = f"judge_high_{output_file_name_B}"
else:
    output_file_name = f"judge_high_{output_file_name_B.split('_')[1]}"
output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_high_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, diff_img1)

print(f"2つの画像の差異部分に枠をつけたカラー画像を{output_file_path}に保存しました")

