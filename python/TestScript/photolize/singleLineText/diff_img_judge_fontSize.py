# 文字の大きさ差異判定（失敗作）
# 参考サイト：https://qiita.com/grv2688/items/44f9e0ddd429afbb26a2
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os


# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイル名を生成
output_file_name_A = 'base.png'
output_file_name_B = 'chg_fontSize.png'
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


#######
# 文字の特徴抽出と比較
text_size_threshold = 10  # 文字の大きさの閾値を設定（適切な値に調整）
# src_ptsとdst_ptsの対応する特徴点を使って、文字の大きさを比較
text_sizes_src = []  # 画像Aの文字の大きさを格納するリスト
text_sizes_dst = []  # 画像Bの文字の大きさを格納するリスト

for src_pt, dst_pt in zip(src_pts, dst_pts):
    x1, y1 = src_pt[0]
    x2, y2 = dst_pt[0]
    
    # 文字の大きさを計算（例: ユークリッド距離）
    text_size = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    text_sizes_src.append(text_size)

# 画像Bの文字の大きさと比較
for dst_pt, src_pt in zip(dst_pts, src_pts):
    x1, y1 = dst_pt[0]
    x2, y2 = src_pt[0]
    
    # 文字の大きさを計算（例: ユークリッド距離）
    text_size = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    text_sizes_dst.append(text_size)

# 文字の大きさの差異を評価
text_size_diff = np.abs(np.array(text_sizes_src) - np.array(text_sizes_dst))

# 差異の閾値を設定して判定
text_size_diff_threshold = 5  # 適切な閾値を設定（大きさの差異が許容範囲内か調整）
if np.any(text_size_diff > text_size_diff_threshold):
    print("文字の大きさに差異があります")
else:
    print("文字の大きさに差異はありません")
#######


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
output_file_name = f"diff_{output_file_name_B.split('_')[1]}"
# output_file_name = f"diff_{current_date}.png"

output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_img/")
# output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_high_png/")

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, result_add)

print(f"2つの画像の差異を示した画像を{output_file_path}に保存しました")
