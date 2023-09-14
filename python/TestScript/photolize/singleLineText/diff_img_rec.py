# 色付けありの差異検出
# 参考サイト：https://qiita.com/grv2688/items/44f9e0ddd429afbb26a2
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os


# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイル名を生成
output_file_name_A = 'base.png'
output_file_name_B = 'chg_position.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)
output_file_path_B = os.path.join(output_dir, output_file_name_B)
imgA = cv2.imread(output_file_path_A)
imgB = cv2.imread(output_file_path_B)
# OpenCVはBGRフォーマットなので、RGBへ変換する
imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)
imgB = cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)
# 画像サイズを取得
hA, wA, cA = imgA.shape[:3]
hB, wB, cA = imgB.shape [:3]

# 特徴量検出器を作成
akaze = cv2.AKAZE_create()
# 二つの画像の特徴点を抽出
kpA, desA = akaze.detectAndCompute(imgA,None)
kpB, desB = akaze.detectAndCompute(imgB,None)

# imageBを透視変換する
# 透視変換: 斜めから撮影した画像を真上から見た画像に変換する感じ
# BFMatcher型のオブジェクトを作成する
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# 記述子をマッチさせる。※スキャン画像(B2)の特徴抽出はforループ前に実施済み。
matches = bf.match(desA,desB)
# マッチしたものを距離順に並べ替える。
matches = sorted(matches, key = lambda x:x.distance)
# マッチしたもの（ソート済み）の中から上位★%（参考：15%)をgoodとする。
good = matches[:int(len(matches) * 0.15)]
# 対応が取れた特徴点の座標を取り出す？
src_pts = np.float32([kpA[m.queryIdx].pt for m in good]).reshape(-1,1,2)
dst_pts = np.float32([kpB[m.trainIdx].pt for m in good]).reshape(-1,1,2)
# findHomography:二つの画像から得られた点の集合を与えると、その物体の投射変換を計算する
M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0) # dst_img作成の際だけ使う。warpperspectiveの使い方がわかってない。
# imgBを透視変換。
imgB_transform = cv2.warpPerspective(imgB, M, (wA, hA))

# imgAとdst_imgの差分を求めてresultとする。グレースケールに変換。
result = cv2.absdiff(imgA, imgB_transform)
result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

# 二値化
_, result_bin = cv2.threshold(result_gray, 50, 255, cv2.THRESH_BINARY) # 閾値は50

# カーネルを準備（オープニング用）
kernel = np.ones((2,2),np.uint8)
# オープニング（収縮→膨張）実行 ノイズ除去
result_bin = cv2.morphologyEx(result_bin, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。

# 二値画像をRGB形式に変換し、2枚の画像を重ねる。
result_bin_rgb = cv2.cvtColor(result_bin, cv2.COLOR_GRAY2RGB)
result_add = cv2.addWeighted(imgA, 0.3, result_bin_rgb, 0.7, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる

### 枠づけ ###
# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_img1 = cv2.subtract(imgA, imgB_transform)
diff_img1_gray = cv2.cvtColor(diff_img1, cv2.COLOR_BGR2GRAY)  # グレースケールに変換

# 二値化
_, diff_img1_bin = cv2.threshold(diff_img1_gray, 50, 255, cv2.THRESH_BINARY)  # 閾値は50

# カーネルを準備（オープニング用）
kernel = np.ones((2, 2), np.uint8)
# オープニング（収縮→膨張）実行 ノイズ除去
diff_img1_bin = cv2.morphologyEx(diff_img1_bin, cv2.MORPH_OPEN, kernel)  # オープニング（収縮→膨張）。ノイズ除去。

# # 差分画像に輪郭を描画
# contours, _ = cv2.findContours(diff_img1_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for c in contours:
#     x, y, w, h = cv2.boundingRect(c)
#     if w > 1 and h > 1:
#         cv2.rectangle(diff_img1, (x, y), (x + w, y + h), (0, 0, 255), 3)  # 赤枠を描画

# ２つの画像の差分を表示
contours, _ = cv2.findContours(diff_img1_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("抽出された輪郭の数:", len(contours))

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 1 and h > 1:
        if imgB[y:y+h, x:x+w].mean() > imgA[y:y+h, x:x+w].mean():
            # 差異が２枚目の画像で大きい場合、赤色で表示
            cv2.rectangle(imgB, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            # 差異が１枚目の画像で大きい場合、緑色で表示
            cv2.rectangle(imgB, (x, y), (x + w, y + h), (0, 255, 0), 3)

# 画像Bから画像Aを引くことで2枚目の画像の差分のみを取得
diff_img2 = cv2.subtract(imgB_transform, imgA)
diff_img2_gray = cv2.cvtColor(diff_img2, cv2.COLOR_BGR2GRAY)  # グレースケールに変換

# 二値化
_, diff_img2_bin = cv2.threshold(diff_img2_gray, 50, 255, cv2.THRESH_BINARY)  # 閾値は50

# カーネルを準備（オープニング用）
kernel = np.ones((2, 2), np.uint8)
# オープニング（収縮→膨張）実行 ノイズ除去
diff_img2_bin = cv2.morphologyEx(diff_img2_bin, cv2.MORPH_OPEN, kernel)  # オープニング（収縮→膨張）。ノイズ除去。

# 差分画像に輪郭を描画
contours, _ = cv2.findContours(diff_img2_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 1 and h > 1:
        cv2.rectangle(diff_img2, (x, y), (x + w, y + h), (0, 0, 255), 3)  # 緑枠を描画

### 変更前と変更後の色分け ###
## 変更前の色付け ##
# 白色の範囲を定義
lower_white = (128, 128, 128)  # 下限（B、G、R）
upper_white = (254, 254, 254)  # 上限（B、G、R）

# 白色の範囲内にあるピクセルをマスクとして取得
white_mask = cv2.inRange(result_add, lower_white, upper_white)

# 新しい色（緑色）を指定
new_color = (0, 255, 0)  # (B、G、R)

# ピクセルの色を変更
result_add[white_mask > 0] = new_color

## 変更後の色付け ##
# 白色の範囲を定義
lower_white = (255, 255, 255)  # 下限（B、G、R）
upper_white = (255, 255, 255)  # 上限（B、G、R）

# 白色の範囲内にあるピクセルをマスクとして取得
white_mask = cv2.inRange(result_add, lower_white, upper_white)

# 新しい色（赤色）を指定
new_color = (0, 0, 255)  # (B、G、R)

# ピクセルの色を変更
result_add[white_mask > 0] = new_color

### 差異が検出されたか判定 ###
# 2値画像（result_bin）の白いピクセル（差分が存在する部分）の数をカウント
white_pixel_count = cv2.countNonZero(result_bin)

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

# 画像を保存する
cv2.imwrite(output_file_path, imgB)

print(f"2つの画像の差異を示した画像を{output_file_path}に保存しました")
