# 成功作
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
output_file_name_A = 'maxChar_Work.png'
output_file_name_B = 'maxChar_notWork.png'
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

# 画像の差分を計算
diff = cv2.absdiff(img1_gray, img2_gray)
ret, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
diff = cv2.GaussianBlur(diff, (11, 11), 0)

### 枠づけ ###
red_rectangles = []  # 赤枠の情報を格納するリスト
green_rectangles = []  # 緑枠の情報を格納するリスト
text_positions = []  # 文字の位置情報を格納するリスト
correct_contours = [] # 適切な枠の情報を格納するリスト
threshold_distance = 100

# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_img1 = cv2.subtract(img1_gray, img2_gray)
diff_img2 = cv2.subtract(img2_gray, img1_gray)

# 二値化
ret, diff_img1 = cv2.threshold(diff_img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
diff_img1 = cv2.GaussianBlur(diff_img1, (11, 11), 0)
ret, diff_img2 = cv2.threshold(diff_img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
diff_img2 = cv2.GaussianBlur(diff_img2, (11, 11), 0)

# 差分画像に輪郭を描画
contours1, _ = cv2.findContours(diff_img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(diff_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
all_contours = contours1 + contours2
print("抽出された枠の数:", len(all_contours))

# 各枠に対して処理を行う
for contour in all_contours:
    x, y, w, h = cv2.boundingRect(contour)
    # 枠の中心座標を計算
    center_x = x + w // 2
    center_y = y + h // 2
    
    # 既存の文字と近くにある場合、同じ枠に追加
    is_added_to_existing = False
    for text_position in text_positions:
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
        text_positions.append([center_x, center_y, x, y, x + w, y + h])

# 適切な枠の情報をもつリストの作成
for position in text_positions:
    x1, y1, x2, y2 = position[2:]
    correct_contours.append([x1, y1, x2-x1, y2-y1])
print("適切な枠の数:", len(correct_contours))

# 枠を描画
for c in correct_contours:
    x, y, w, h = c
    
    if w > 1 and h > 1:
        if img2[y:y+h, x:x+w].mean() > img1[y:y+h, x:x+w].mean():
            # 差異が２枚目の画像で大きい場合、赤色で表示
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 3)
            red_rectangles.append((x, y, w, h))
        else:
            # 差異が１枚目の画像で大きい場合、緑色で表示
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 4)
            green_rectangles.append((x, y, w, h))

# 赤枠の座標をy座標が0に近い順、次にx座標が0に近い順にソート
red_rectangles.sort(key=lambda rect: (rect[1], rect[0]))
# 緑枠の座標をy座標が0に近い順、次にx座標が0に近い順にソート
green_rectangles.sort(key=lambda rect: (rect[1], rect[0]))

# 赤枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(red_rectangles, start=1):
    cv2.putText(img2, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    print(f"赤枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# 緑枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(green_rectangles, start=1):
    cv2.putText(img2, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    print(f"緑枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# 対応する赤枠と緑枠を表示
match_list = []  # マッチング結果を格納するリスト
for i, (x1, y1, w1, h1) in enumerate(red_rectangles, start=1):
    min_distance = float('inf')  # 最小距離を初期化
    closest_green_rect_index = None  # 最も近い緑枠のインデックスを初期化
    
    for j, (x2, y2, w2, h2) in enumerate(green_rectangles, start=1):
        # 赤枠と緑枠の中心座標を計算
        center_x1 = x1 + w1 // 2
        center_y1 = y1 + h1 // 2
        center_x2 = x2 + w2 // 2
        center_y2 = y2 + h2 // 2
        
        # 中心座標間の距離を計算
        distance = np.sqrt((center_x1 - center_x2)**2 + (center_y1 - center_y2)**2)
        
        if distance < 650 and distance < min_distance:  # 適切な距離の閾値を設定
            min_distance = distance
            closest_green_rect_index = j-1
    
    if closest_green_rect_index is not None:
        match_list.append((i, closest_green_rect_index+1, red_rectangles[i-1], green_rectangles[closest_green_rect_index]))
        print(f"赤枠{i:2} と緑枠{closest_green_rect_index+1:2} は対応します")

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
cv2.imwrite(output_file_path, img2)

print(f"2つの画像の差異部分に枠をつけたカラー画像を{output_file_path}に保存しました")

