# 成功作
# 連番の色枠付き画像を生成＆対応する赤枠と緑枠を出力＆赤枠と緑枠の座標と幅と高さを出力＆配置の差異判定
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np
import subprocess
import math

# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイル名を生成
output_file_name_A = 'before.png'
output_file_name_B = 'after.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)
output_file_path_B = os.path.join(output_dir, output_file_name_B)

img1 = cv2.imread(output_file_path_A)
img2 = cv2.imread(output_file_path_B)

# clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# img1_gray = clahe.apply(img1_gray)
# img2_gray = clahe.apply(img2_gray)

# img1_gray = cv2.GaussianBlur(img1_gray, (13, 13), 0)
# img2_gray = cv2.GaussianBlur(img2_gray, (13, 13), 0)

# print("img1_gray shape:", img1_gray.shape)
# print("img2_gray shape:", img2_gray.shape)


# width = 3423
# height = 3484
# # 画像のサイズを一致させる
# img1_gray = cv2.resize(img1_gray, (width, height))  # widthとheightは適切なサイズに置き換える
# img2_gray = cv2.resize(img2_gray, (width, height))

# 画像の差分を計算
diff = cv2.absdiff(img1_gray, img2_gray)
ret, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
diff = cv2.GaussianBlur(diff, (11, 11), 0)

### 枠づけ ###
red_rectangles = []  # 赤枠の情報を格納するリスト
green_rectangles = []  # 緑枠の情報を格納するリスト
text_positions1 = []  # 変更前画像から変更後画像を引いた差分画像における、文字の位置情報を格納するリスト
text_positions2 = []  # 変更後画像から変更前画像を引いた差分画像における、文字の位置情報を格納するリスト
all_text_positions = []  # 上記２つのリストを足し合わせた、文字の位置情報を格納するリスト
correct_contours1 = [] # text_position1の枠の中心座標を取り除いた、枠の情報を格納するリスト
correct_contours2 = [] # text_position2の枠の中心座標を取り除いた、枠の情報を格納するリスト
threshold_distance = 100

# 二値化
ret, img1_bin = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img1_bin = cv2.GaussianBlur(img1_bin, (11, 11), 0)
ret, img2_bin = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img2_bin = cv2.GaussianBlur(img2_bin, (11, 11), 0)

# 白黒を逆にする
img1_bin_reverse = cv2.bitwise_not(img1_bin)
img2_bin_reverse = cv2.bitwise_not(img2_bin)

# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_before = cv2.subtract(img1_bin_reverse, img2_bin_reverse)
diff_after = cv2.subtract(img2_bin_reverse, img1_bin_reverse)

# 差分画像に輪郭を描画
contours1, _ = cv2.findContours(diff_before, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(diff_after, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
all_contours = contours1 + contours2
print("抽出された枠の数:", len(all_contours))

# 各枠に対して処理を行う
for contour in contours1:
    x, y, w, h = cv2.boundingRect(contour)
    # 枠の中心座標を計算
    center_x = x + w // 2
    center_y = y + h // 2
    
    # 既存の文字と近くにある場合、同じ枠に追加
    is_added_to_existing = False
    for text_position in text_positions1:
        dist = np.sqrt((center_x - text_position[0]) ** 2 + (center_y - text_position[1]) ** 2)
        if dist < threshold_distance:  # 適切な距離の閾値を設定
            text_position[0] = (text_position[0] + center_x) // 2  # 中心座標を更新
            text_position[1] = (text_position[1] + center_y) // 2
            text_position[2] = min(text_position[2], x)  # 枠の左上座標を更新
            text_position[3] = min(text_position[3], y)
            text_position[4] = max(text_position[4], x + w)  # 枠の右下座標を更新
            text_position[5] = max(text_position[5], y + h)
            is_added_to_existing = True
            break
    
    # 新しい枠として追加
    if not is_added_to_existing:
        text_positions1.append([center_x, center_y, x, y, x + w, y + h])

        # 各枠に対して処理を行う
for contour in contours2:
    x, y, w, h = cv2.boundingRect(contour)
    # 枠の中心座標を計算
    center_x = x + w // 2
    center_y = y + h // 2
    
    # 既存の文字と近くにある場合、同じ枠に追加
    is_added_to_existing = False
    for text_position in text_positions2:
        dist = np.sqrt((center_x - text_position[0]) ** 2 + (center_y - text_position[1]) ** 2)
        if dist < threshold_distance:  # 適切な距離の閾値を設定
            text_position[0] = (text_position[0] + center_x) // 2  # 中心座標を更新
            text_position[1] = (text_position[1] + center_y) // 2
            text_position[2] = min(text_position[2], x)  # 枠の左上座標を更新
            text_position[3] = min(text_position[3], y)
            text_position[4] = max(text_position[4], x + w)  # 枠の右下座標を更新
            text_position[5] = max(text_position[5], y + h)
            is_added_to_existing = True
            break
    
    # 新しい枠として追加
    if not is_added_to_existing:
        text_positions2.append([center_x, center_y, x, y, x + w, y + h])

all_text_positions = text_positions1 + text_positions2

# 適切な枠の情報をもつリストの作成
for position in text_positions1:
    x1, y1, x2, y2 = position[2:]
    correct_contours1.append([x1, y1, x2-x1, y2-y1])

# 適切な枠の情報をもつリストの作成
for position in text_positions2:
    x1, y1, x2, y2 = position[2:]
    correct_contours2.append([x1, y1, x2-x1, y2-y1])

print("検出された枠ペア数:", int(len(all_text_positions)/2))

# # 枠を描画
# for c in correct_contours:
#     x, y, w, h = c
    
#     if w > 1 and h > 1:
#         if img2[y:y+h, x:x+w].mean() > img1[y:y+h, x:x+w].mean():
#             # 差異が２枚目の画像で大きい場合、赤色で表示
#             cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 3)
#             red_rectangles.append((x, y, w, h))
#         else:
#             # 差異が１枚目の画像で大きい場合、緑色で表示
#             cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 4)
#             green_rectangles.append((x, y, w, h))

# 枠を描画
for c in correct_contours1:
    x, y, w, h = c

    if w > 1 and h > 1:
        # 差異が２枚目の画像で大きい場合、赤色で表示
        cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 3)
        red_rectangles.append((x, y, w, h))

# 枠を描画
for c in correct_contours2:
    x, y, w, h = c

    if w > 1 and h > 1:
        # 差異が１枚目の画像で大きい場合、緑色で表示
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 4)
        green_rectangles.append((x, y, w, h))

# red_rectangles の各矩形を x^2 + y^2 の和で昇順にソートする
red_rectangles.sort(key=lambda rect: math.sqrt(rect[0]**2 + rect[1]**2))
# red_rectangles の各矩形を x^2 + y^2 の和で昇順にソートする
green_rectangles.sort(key=lambda rect: math.sqrt(rect[0]**2 + rect[1]**2))

# 対応する赤枠と緑枠を表示
match_list = []  # マッチング結果を格納するリスト
used_green_rect_indices = set()  # すでに対応付けされた緑枠のインデックスを格納する集合
for i, (x1, y1, w1, h1) in enumerate(red_rectangles, start=1):
    min_distance = float('inf')  # 最小距離を初期化
    closest_green_rect_index = None  # 最も近い緑枠のインデックスを初期化
    
    for j, (x2, y2, w2, h2) in enumerate(green_rectangles, start=1):
        if j-1 in used_green_rect_indices:  # すでに対応付けされた緑枠はスキップする
            continue
        
        # 赤枠と緑枠の中心座標を計算
        center_x1 = x1 + w1 // 2
        center_y1 = y1 + h1 // 2
        center_x2 = x2 + w2 // 2
        center_y2 = y2 + h2 // 2
        
        # 中心座標間の距離を計算
        distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
        
        if distance < 850 and distance < min_distance:  # 適切な距離の閾値を設定
            min_distance = distance
            closest_green_rect_index = j-1
    
    if closest_green_rect_index is not None:
        match_list.append((i, closest_green_rect_index+1, red_rectangles[i-1], green_rectangles[closest_green_rect_index]))
        used_green_rect_indices.add(closest_green_rect_index)  # 対応付けされた緑枠のインデックスを集合に追加する
        print(f"赤枠{i:2} と緑枠{closest_green_rect_index+1:2} は対応します")
        

# # 対応する赤枠と緑枠を表示
# match_list = []  # マッチング結果を格納するリスト
# for i, (x1, y1, w1, h1) in enumerate(red_rectangles, start=1):
#     min_distance = float('inf')  # 最小距離を初期化
#     closest_green_rect_index = None  # 最も近い緑枠のインデックスを初期化
#     # 赤枠の中心座標を計算
#     center_x1 = x1 + w1 // 2
#     center_y1 = y1 + h1 // 2
    
#     for j, (x2, y2, w2, h2) in enumerate(green_rectangles, start=1):
#         # 緑枠の中心座標を計算
#         center_x2 = x2 + w2 // 2
#         center_y2 = y2 + h2 // 2
        
#         # 中心座標間の距離を計算
#         distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
#         # print(f"(赤枠{i}, 緑枠{j})のdistance: {distance}")
#         if distance < 650 and distance < min_distance:  # 適切な距離の閾値を設定
#             min_distance = distance
#             closest_green_rect_index = j-1
    
#     if closest_green_rect_index is not None:
#         match_list.append((i, closest_green_rect_index+1, red_rectangles[i-1], green_rectangles[closest_green_rect_index]))
#         print(f"赤枠{i:2} と緑枠{closest_green_rect_index+1:2} は対応します")

# 赤枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(red_rectangles, start=1):
    cv2.putText(img1, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    print(f"赤枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# 緑枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(green_rectangles, start=1):
    cv2.putText(img2, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    print(f"緑枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")



### 差異が検出されたか判定 ###
# ある閾値以上の白いピクセルが存在する場合、差分があると判断する
threshold = 100  # 適切な閾値を選択
red_text_start = "\033[91m"
red_text_end = "\033[0m"
green_text_start = "\033[92m"
green_text_end = "\033[0m"

# 座標の違いから配置の差異を検出
# match_listを使用して、赤枠と緑枠の座標の差を求める
count = 0
# 幅と高さの差の許容誤差
tolerance = 5
for i, (red_point, green_point, red_rect, green_rect) in enumerate(match_list, start=1):
    x1, y1, w1, h1 = red_rect
    x2, y2, w2, h2 = green_rect
    
    # 赤枠と緑枠の座標の差を計算
    x_diff = x1 - x2
    y_diff = y1 - y2
    w_diff = w1 - w2
    h_diff = h1 - h2

    # 幅と高さの差が許容誤差以内のとき
    if abs(w_diff) <= tolerance and abs(h_diff) <= tolerance:
        # x座標またはy座標の差が0以外のとき
        if x_diff != 0 or y_diff != 0:
            count += 1 # いくつ差異箇所があったかをカウント
        
        # 差を表示
        print(f"(赤枠{red_point}, 緑枠{green_point}): x座標差={abs(x_diff):5}, y座標差={abs(y_diff):5}, 幅差={abs(w_diff):2}, 高低差={abs(h_diff):2}")

if count > 0:
    print(f"{red_text_start}配置の差異を {count} 箇所検出しました{red_text_end}")
else:
    print(f"{green_text_start}配置の差異はありません{green_text_end}")

# 差分画像を保存
output_file_name1 = "before.png"
output_file_name2 = "after.png"
output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)
    command = f"sudo chown -R aridome:aridome {output_dir2}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name1)

# 画像を保存する
cv2.imwrite(output_file_path, img1)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name2)

# 画像を保存する
cv2.imwrite(output_file_path, img2)

print(f"2つの画像の差異部分に枠をつけたカラー画像をに保存しました")

