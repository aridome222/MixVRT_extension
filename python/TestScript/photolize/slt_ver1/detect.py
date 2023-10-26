# 成功作（入力画面から入力欄の枠を抽出し、元画像にその枠を重ね合わせ＆枠の座標情などを取得）
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
output_file_name_A = '5_input.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)

img1 = cv2.imread(output_file_path_A)

# BGRからHSVに変換
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

# # 薄水色のHSVの範囲
# hsv_min = np.array([90, 3, 0])
# hsv_max = np.array([110, 9, 255])

# 薄水色のHSVの範囲# [色相, 彩度, 明度]
hsv_min = np.array([90, 3, 0]) 
hsv_max = np.array([110, 20, 255])

# マスク画像を作成
mask = cv2.inRange(hsv, hsv_min, hsv_max)

# マスクされた画像を作成
masked_img1 = cv2.bitwise_and(img1, img1, mask=mask)

# カラー画像をグレースケール画像に変換
masked_img1_gray = cv2.cvtColor(masked_img1, cv2.COLOR_BGR2GRAY)

# マスク画像から白い領域の輪郭を検出する
contours, hierarchy = cv2.findContours(masked_img1_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

selected_contours = []
for cnt in contours:
    if cv2.contourArea(cnt)>1000: #数字は試行錯誤が必要
        epsilon = 0.01*cv2.arcLength(cnt,True) #数字は試行錯誤が必要
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        selected_contours.append(approx)

# 別の画像に輪郭を描画する
# result = np.zeros_like(img1)
cv2.drawContours(img1, selected_contours, -1, color=255, thickness=2)

# 輪郭に番号を付ける
font = cv2.FONT_HERSHEY_SIMPLEX # フォントの種類
font_size = 0.5 # フォントのサイズ
font_color = (0, 0, 255) # フォントの色（BGR）
for i, cnt in enumerate(selected_contours):
    x, y, w, h = cv2.boundingRect(cnt) # 矩形領域の座標と幅と高さを取得
    cv2.putText(img1, str(i+1), (x+w//2, y+h//2), font, font_size, font_color) # 矩形領域の中心に番号を描画

# # 輪郭から矩形領域の座標情報を取得する
# rectangles = []
# for cnt in selected_contours:
#     x, y, w, h = cv2.boundingRect(cnt) # x, yは左上の座標、w, hは幅と高さ
#     rectangles.append((x, y, w, h))

# # 矩形領域の座標情報を表示する
# print(rectangles)

# 輪郭から矩形領域の座標情報を取得する
rectangles = []
for cnt in selected_contours:
    x, y, w, h = cv2.boundingRect(cnt) # x, yは左上の座標、w, hは幅と高さ
    rectangles.append((x, y, w, h))

# 矩形領域の数をカウント
num_rectangles = len(rectangles)
print(f"＜入力欄の数＞: {num_rectangles}個\n")

# 矩形領域の座標情報をひとつずつ表示する
for i, rect in enumerate(rectangles):
    print(f"入力欄{i+1}の座標: ({rect[0]}, {rect[1]})")
    print(f"入力欄{i+1}の幅: {rect[2]}")
    print(f"入力欄{i+1}の高さ: {rect[3]}")
    print()


# img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# # 二値化
# ret, img1_bin = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # カーネルを準備（オープニング用）
# kernel = np.ones((2,2),np.uint8)
# # オープニング（収縮→膨張）実行 ノイズ除去
# result_bin1 = cv2.morphologyEx(img1_bin, cv2.MORPH_OPEN, kernel) # オープニング（収縮→膨張）。ノイズ除去。

# # 適応的閾値処理を行う（各ピクセルの周囲の領域におけるガウシアン重みつき平均値を採用、画像のコントラストが比較的高い場合に適している）
# result_bin1 = cv2.adaptiveThreshold(img1_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
# # 適応的閾値処理を行う（各ピクセルの周囲の領域における平均値を採用、画像のコントラストが低い場合に有用で、ノイズに対して頑健）
# result_bin1 = cv2.adaptiveThreshold(img1_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# # エッジ検出を行う 
# threshold1 = 100
# threshold2 = 300
# edges1 = cv2.Canny(result_bin1, threshold1, threshold2)  # 適切な閾値を設定

# # 二値画像をRGB形式に変換
# result_bin1_rgb = cv2.cvtColor(edges1, cv2.COLOR_GRAY2RGB)

# ### 変更前と変更後の色分け ###
# # 白色の範囲を定義
# lower_white = np.array([200, 200, 200])  # 下限（B、G、R）
# upper_white = np.array([255, 255, 255])  # 上限（B、G、R）

# # 白色の範囲内にあるピクセルをマスクとして取得
# white_mask1 = cv2.inRange(result_bin1_rgb, lower_white, upper_white)

# # 緑色を指定
# green_color = (0, 255, 0)  # (B、G、R)
# # 赤色を指定
# red_color = (0, 0, 255)  # (B、G、R)

# # ピクセルの色を変更
# result_bin1_rgb[white_mask1 > 0] = red_color

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

