# 成功作
# 連番の色枠付き画像を生成＆対応する赤枠と緑枠を出力＆赤枠と緑枠の座標と幅と高さを出力＆配置の差異判定
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np
import subprocess
import math


RED_TEXT_START = "\033[91m"
RED_TEXT_END = "\033[0m"
GREEN_TEXT_START = "\033[92m"
GREEN_TEXT_END = "\033[0m"


def str_red(text):
    """
    文字列を赤色で装飾する関数

    Parameters:
    - text (str): 装飾する文字列

    Returns:
    - decorated_text (str): 赤色で装飾された文字列
    """
    # return text
    return f"{RED_TEXT_START}{text}{RED_TEXT_END}"


def str_green(text):
    """
    文字列を緑色で装飾する関数

    Parameters:
    - text (str): 装飾する文字列

    Returns:
    - decorated_text (str): 緑色で装飾された文字列
    """
    # return text
    return f"{GREEN_TEXT_START}{text}{GREEN_TEXT_END}"


def update_text_positions(contour, text_positions, threshold_distance=100):
    """
    検出した枠において、近い枠同士を結合する関数

    Parameters:
    - contour (list): 検出した輪郭の座標情報
    - text_positions (list): 既存のテキスト位置情報が格納されたリスト
    - threshold_distance (int): 枠を結合するための距離の閾値

    Description:
    与えられた検出した輪郭と既存のテキスト位置情報を比較し、
    近い枠同士を結合する。結合された場合は既存のテキスト位置情報を更新し、
    結合されない場合は新しいテキスト位置情報を追加する。
    """
    x, y, w, h = cv2.boundingRect(contour)
    center_x, center_y = x + w // 2, y + h // 2
    
    is_added_to_existing = False
    for text_position in text_positions:
        dist = np.sqrt((center_x - text_position[0]) ** 2 + (center_y - text_position[1]) ** 2)
        if dist < threshold_distance:
            text_position[0] = (text_position[0] + center_x) // 2
            text_position[1] = (text_position[1] + center_y) // 2
            text_position[2] = min(text_position[2], x)
            text_position[3] = min(text_position[3], y)
            text_position[4] = max(text_position[4], x + w)
            text_position[5] = max(text_position[5], y + h)
            is_added_to_existing = True
            break
    
    if not is_added_to_existing:
        text_positions.append([center_x, center_y, x, y, x + w, y + h])


def filter_contours_by_area(contours, threshold_area=150):
    """
    一定の面積以下の輪郭を除外する関数

    Parameters:
    - contours (list): 輪郭情報が格納されたリスト
    - threshold_area (int): 一定の面積の閾値（適宜調整する）

    Returns:
    - filtered_contours (list): 面積が閾値以上の輪郭のみを格納したリスト
    """

    filtered_contours = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > threshold_area:
            filtered_contours.append(contour)
    
    return filtered_contours


def match_red_and_green_rectangles(red_rectangles, green_rectangles, distance_threshold=850):
    """
    赤枠と緑枠の対応付けを行う関数

    Parameters:
    - red_rectangles (list): 赤枠の座標情報が格納されたリスト
    - green_rectangles (list): 緑枠の座標情報が格納されたリスト
    - distance_threshold (int): 赤枠と緑枠を対応付けるための距離の閾値（適宜調整する）

    Returns:
    - match_list (list): マッチング結果を格納したリスト
    """

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

            if distance < distance_threshold and distance < min_distance:
                min_distance = distance
                closest_green_rect_index = j-1

        if closest_green_rect_index is not None:
            match_list.append((i, closest_green_rect_index+1, red_rectangles[i-1], green_rectangles[closest_green_rect_index]))
            used_green_rect_indices.add(closest_green_rect_index)  # 対応付けされた緑枠のインデックスを集合に追加する

    print("\n【 対応する枠ペア情報 】")
    print(f"・枠ペアの数: {int(len(match_list))}")
    for match in match_list:
        red_index, green_index, red_rect, green_rect = match
        print(f"・{str_red('赤枠')}{red_index:2} と{str_green('緑枠')}{green_index:2} は対応します")
        
        # 赤枠の座標情報
        red_x, red_y, red_w, red_h = red_rect
        print(f"    赤枠: 左上({red_x}, {red_y}), 幅{red_w}, 高さ{red_h}")
        
        # 緑枠の座標情報
        green_x, green_y, green_w, green_h = green_rect
        print(f"    緑枠: 左上({green_x}, {green_y}), 幅{green_w}, 高さ{green_h}")
    print("")

    return match_list


def detect_pos_diff(match_list, tolerance=5):
    """
    配置の差異を検出する関数

    Parameters:
    - match_list (list): マッチング結果が格納されたリスト
    - tolerance (int): 幅と高さの差の許容誤差

    Returns:
    - count (int): 配置の差異が検出された箇所の数
    """
    count = 0

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
                count += 1  # いくつ差異箇所があったかをカウント

                # 差を表示
                print(f"({str_red('赤枠')}{red_point}, {str_green('緑枠')}{green_point}): "
                      f"x座標差={abs(x_diff):5}, y座標差={abs(y_diff):5}, 幅差={abs(w_diff):2}, 高低差={abs(h_diff):2}")

    return count


""" 

    前処理（画像の読み込み＆画像処理）

"""
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

# 画像読み込み
before_img = cv2.imread(output_file_path_A)
after_img = cv2.imread(output_file_path_B)

# 画像処理（グレースケール化＆平滑化＆ぼかし）
before_gray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after_img, cv2.COLOR_BGR2GRAY)

# ヒストグラム均等化は全ての画素の輝度値を均等に分布する。
# 画像内の局所的な部分（極端に明るいor暗い部分）があると、
# その部分のコントラスが強調されてしまう。
# また、ノイズが強い場合、均等化によりノイズが増幅されてしまう。
# clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
# before_gray = clahe.apply(before_gray)
# after_gray = clahe.apply(after_gray)

# before_gray = cv2.GaussianBlur(before_gray, (11, 11), 0)
# after_gray = cv2.GaussianBlur(after_gray, (11, 11), 0)

# 画像の差分を計算
diff = cv2.absdiff(before_gray, after_gray)
ret, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# diff = cv2.GaussianBlur(diff, (11, 11), 0)

### 枠づけ ###
red_rectangles = []  # 赤枠の情報を格納するリスト
green_rectangles = []  # 緑枠の情報を格納するリスト
text_positions_before = []  # 変更前画像から変更後画像を引いた差分画像における、文字の位置情報を格納するリスト
text_positions_after = []  # 変更後画像から変更前画像を引いた差分画像における、文字の位置情報を格納するリスト
all_text_positions = []  # 上記２つのリストを足し合わせた、文字の位置情報を格納するリスト
correct_contours_before = [] # 赤枠の情報（左上隅座標(x, y)と幅、高さ）を格納するリスト
correct_contours_after = [] # 緑枠の情報（左上隅座標(x, y)と幅、高さ）を格納するリスト

# 二値化
ret, before_bin = cv2.threshold(before_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
before_bin = cv2.GaussianBlur(before_bin, (11, 11), 0)
ret, after_bin = cv2.threshold(after_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
after_bin = cv2.GaussianBlur(after_bin, (11, 11), 0)

# 白黒を逆にする
before_bin_reverse = cv2.bitwise_not(before_bin)
after_bin_reverse = cv2.bitwise_not(after_bin)

# 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
diff_before = cv2.subtract(before_bin_reverse, after_bin_reverse)
diff_after = cv2.subtract(after_bin_reverse, before_bin_reverse)


""" 

    差分検出

"""
# 差分画像内の輪郭を検出
contours_before, _ = cv2.findContours(diff_before, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_after, _ = cv2.findContours(diff_after, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
all_contours = contours_before + contours_after
print("\n---------------------------差分検出結果---------------------------")
print("【 各処理後の枠数 】")
print(f"・検出した{str_red('赤枠')}の数: {len(contours_before)}")
print(f"・検出した{str_green('緑枠')}の数: {len(contours_after)}")

# 面積が一定以下の輪郭を除外
filtered_contours_before = filter_contours_by_area(contours_before)
filtered_contours_after = filter_contours_by_area(contours_after)
filtered_all_contours = filtered_contours_before + filtered_contours_after
print(f"・ノイズ除去後の{str_red('赤枠')}の数: {len(filtered_contours_before)}")
print(f"・ノイズ除去後の{str_green('緑枠')}の数: {len(filtered_contours_after)}")

# 赤枠に対して処理を行う
for contour in filtered_contours_before:
    update_text_positions(contour, text_positions_before)
# 緑枠に対して処理を行う
for contour in filtered_contours_after:
    update_text_positions(contour, text_positions_after)
all_text_positions = text_positions_before + text_positions_after
print(f"・近接枠結合後の{str_red('赤枠')}の数: {len(text_positions_before)}")
print(f"・近接枠結合後の{str_green('緑枠')}の数: {len(text_positions_after)}")

# 枠の左上隅座標・幅・高さの情報をもつリストの作成
for position in text_positions_before:
    x1, y1, x2, y2 = position[2:]
    correct_contours_before.append([x1, y1, x2-x1, y2-y1])

# 枠の左上隅座標・幅・高さの情報をもつリストの作成
for position in text_positions_after:
    x1, y1, x2, y2 = position[2:]
    correct_contours_after.append([x1, y1, x2-x1, y2-y1])

# 赤枠を描画
for c in correct_contours_before:
    x, y, w, h = c

    if w > 1 and h > 1:
        # 差異が２枚目の画像で大きい場合、赤色で表示
        cv2.rectangle(before_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        red_rectangles.append((x, y, w, h))

# 緑枠を描画
for c in correct_contours_after:
    x, y, w, h = c

    if w > 1 and h > 1:
        # 差異が１枚目の画像で大きい場合、緑色で表示
        cv2.rectangle(after_img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        green_rectangles.append((x, y, w, h))

# red_rectangles の各矩形を x^2 + y^2 の和で昇順にソートする
red_rectangles.sort(key=lambda rect: math.sqrt(rect[0]**2 + rect[1]**2))
# red_rectangles の各矩形を x^2 + y^2 の和で昇順にソートする
green_rectangles.sort(key=lambda rect: math.sqrt(rect[0]**2 + rect[1]**2))

# 対応する赤枠と緑枠を見つけて表示する
match_list = match_red_and_green_rectangles(red_rectangles, green_rectangles)

# 赤枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(red_rectangles, start=1):
    cv2.putText(before_img, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # print(f"赤枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")

# 緑枠に番号を割り振りながら座標を出力
for i, (x, y, w, h) in enumerate(green_rectangles, start=1):
    cv2.putText(after_img, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    # print(f"緑枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")


""" 

    差分の種類判定

"""
### 配置の差分が検出されたか判定 ###
# 対応する枠ペアに対して、座標の違いから配置の差分を検出
# diff_pos_count = detect_pos_diff(match_list)
# if diff_pos_count > 0:
#     print(f"{RED_TEXT_START}配置の差異を {diff_pos_count} 箇所検出しました{RED_TEXT_END}")
# else:
#     print(f"{GREEN_TEXT_START}配置の差異はありません{GREEN_TEXT_END}")

""" 

    後処理（差分画像を保存）

"""
### 差分画像を保存 ###
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
cv2.imwrite(output_file_path, before_img)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name2)

# 画像を保存する
cv2.imwrite(output_file_path, after_img)

print("------------------------------------------------------------------\n")

print(f"2つの画像の差異部分に枠をつけた画像を{output_dir2}に保存しました")
