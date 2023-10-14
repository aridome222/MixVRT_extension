# 成功作（画像全体をエッジ抽出する）
# diff_color_img.pyをより正確に差分ごとに色分けできるようにしたもの
# 成功作
# 連番の色枠付き画像を生成＆対応する赤枠と緑枠を出力＆赤枠と緑枠の座標と幅と高さを出力＆配置の差異判定
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np
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
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)

img1 = cv2.imread(output_file_path_A)

# コントラストと明るさを調整する
alpha = 2.0 # コントラストのスケールファクター
beta = 50 # 明るさのオフセット
dst = cv2.convertScaleAbs(img1, alpha=alpha, beta=beta)

img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# # 二値化
# ret, img1_bin = cv2.threshold(img1_gray,0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 二値化
ret, img1_bin = cv2.threshold(img1_gray,0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # 閾値を半分にする
# ret = ret / 2
# # 再度二値化
# ret, img1_bin = cv2.threshold(img1_gray,ret, 255, cv2.THRESH_BINARY)
# # 閾値を半分にする
# ret = ret / 2
# # 再度二値化
# ret, img1_bin = cv2.threshold(img1_gray,ret, 255, cv2.THRESH_BINARY)
# # 閾値を半分にする
# ret = ret / 2
# # 再度二値化
# ret, img1_bin = cv2.threshold(img1_gray,ret, 255, cv2.THRESH_BINARY)
# # 閾値を半分にする
# ret = ret / 2
# # 再度二値化
# ret, img1_bin = cv2.threshold(img1_gray,ret, 255, cv2.THRESH_BINARY)
# # 閾値を半分にする
# ret = ret / 2
# # 再度二値化
# ret, img1_bin = cv2.threshold(img1_gray,ret, 255, cv2.THRESH_BINARY)

# カーネルを準備（オープニング用）
kernel = np.ones((2,2),np.uint8)
# オープニング（収縮→膨張）実行 ノイズ除去
result_bin1 = cv2.morphologyEx(img1_bin, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。

# エッジ検出を行う 
threshold1 = 100
threshold2 = 300
edges1 = cv2.Canny(result_bin1, threshold1, threshold2)  # 適切な閾値を設定

# 二値画像をRGB形式に変換
result_bin1_rgb = cv2.cvtColor(edges1, cv2.COLOR_GRAY2RGB)

### 変更前と変更後の色分け ###
# 白色の範囲を定義
lower_white = np.array([200, 200, 200])  # 下限（B、G、R）
upper_white = np.array([255, 255, 255])  # 上限（B、G、R）

# 白色の範囲内にあるピクセルをマスクとして取得
white_mask1 = cv2.inRange(result_bin1_rgb, lower_white, upper_white)

# 緑色を指定
green_color = (0, 255, 0)  # (B、G、R)
# 赤色を指定
red_color = (0, 0, 255)  # (B、G、R)

# ピクセルの色を変更
result_bin1_rgb[white_mask1 > 0] = red_color

# 差分画像を保存
if output_file_name_A == "base.png":
    output_file_name = f"judge_high_{output_file_name_A}"
else:
    output_file_name = f"judge_high_{output_file_name_A.split('_')[1]}"
output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_high_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)
    command = f"sudo chown -R aridome:aridome {output_dir2}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, img1)

print(f"2つの画像の差異部分に枠をつけたカラー画像を{output_file_path}に保存しました")

