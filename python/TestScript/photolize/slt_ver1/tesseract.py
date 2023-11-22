# 成功作
# AzureOCRを用いた、画像内のテキストの矩形検出＆描画
# azure.cognitiveservices.vision.computervisionを使用
# Tesseractよりかは断然良い
# ただ、まだテキスト輪郭の検出が微妙

import cv2
import os
import numpy as np
import subprocess
import math
import pytesseract

import time
import io


# 色コード
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


def filter_contours_by_area(contours, threshold_area=100):
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


# def get_text_and_pos(path):
#     """
#     画像からテキストの内容と位置を返す関数

#     Parameters:
#     -  path (str): 画像のパス

#     Returns:
#     - text_list (list): テキストの内容が格納されたリスト
#     - position_list (list): テキストの位置が格納されたリスト
#     """

#     # 画像を読み込む
#     img = cv2.imread(path)

#     # 画像の形式を取得する
#     _, ext = os.path.splitext(path) # 拡張子を取得する
#     ext = ext.lower() # 小文字に変換する
#     if ext in [".jpg", ".jpeg"]: # JPEG形式の場合
#         format = ".jpg"
#     elif ext in [".png"]: # PNG形式の場合
#         format = ".png"
#     else: # その他の形式の場合
#         format = ".png" # PNG形式に変換する

#     # 画像を指定した形式にエンコードする
#     _, img_encoded = cv2.imencode(format, img)

#     # 画像をバイト列に変換する
#     img_bytes = io.BytesIO(img_encoded)

#     # readメソッドを呼び出して、非同期に画像からテキストを抽出する
#     # 引数には、画像のストリームと言語を指定する
#     # raw=Trueとすることで、レスポンスのヘッダーにオペレーションIDが含まれる
#     response = client.read_in_stream(img_bytes, language="auto", raw=True)
#     # response = client.read_in_stream(img_bytes, language="ja", raw=True)
#     # response = client.read_in_stream(img_bytes, language="en", raw=True)

#     # 結果を取得するためのオペレーションIDを取得する
#     # ヘッダーのOperation-LocationからオペレーションIDを抽出する
#     operation_location = response.headers["Operation-Location"]
#     operation_id = operation_location.split("/")[-1]

#     # 結果が準備できるまで待つ
#     # get_read_resultメソッドで結果のステータスを確認する
#     # ステータスがnot_startedまたはrunningでなければ、結果が準備できたと判断する
#     # 1秒ごとにステータスを確認する
#     while True:
#         result = client.get_read_result(operation_id)
#         if result.status not in [OperationStatusCodes.not_started, OperationStatusCodes.running]:
#             break
#         time.sleep(1)

#     # 結果を返す
#     if result.status == OperationStatusCodes.succeeded:
#         # テキストの内容と位置を格納するリストを作成する
#         text_list = []
#         position_list = []
#         # 画像内の各テキスト行に対して
#         for line in result.analyze_result.read_results[0].lines:
#             # テキストの内容と位置を取得する
#             text = line.text
#             bbox = line.bounding_box
#             # テキストの内容と位置をリストに追加する
#             text_list.append(text)
#             position_list.append(bbox)
#         # テキストの内容と位置のリストを返す
#         return text_list, position_list
#     else:
#         # エラーが発生した場合は、Noneを返す
#         return None


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
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)

# 画像読み込み
img = cv2.imread(output_file_path_A)

# 画像処理（グレースケール化＆平滑化＆ぼかし）
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ヒストグラム均等化は全ての画素の輝度値を均等に分布する。
# 画像内の局所的な部分（極端に明るいor暗い部分）があると、
# その部分のコントラスが強調されてしまう。
# また、ノイズが強い場合、均等化によりノイズが増幅されてしまう。
# clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
# img_gray = clahe.apply(img_gray)

# img_gray = cv2.GaussianBlur(img_gray, (11, 11), 0)

### 枠づけ ###
red_rectangles = []  # 赤枠の情報を格納するリスト
green_rectangles = []  # 緑枠の情報を格納するリスト
text_positions = []  # 変更前画像から変更後画像を引いた差分画像における、文字の位置情報を格納するリスト
all_text_positions = []  # 上記２つのリストを足し合わせた、文字の位置情報を格納するリスト
correct_contours = [] # 赤枠の情報（左上隅座標(x, y)と幅、高さ）を格納するリスト

# 二値化
ret, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# img_bin = cv2.GaussianBlur(img_bin, (11, 11), 0)

# 白黒を逆にする
img_bin_reverse = cv2.bitwise_not(img_bin)


""" 

    差分検出

"""
# # 差分画像内の輪郭を検出
# contours, hierarchy = cv2.findContours(img_bin_reverse, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# # contours, hierarchy = cv2.findContours(img_bin_reverse, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# internal_contours = [contour for contour in contours if len(cv2.approxPolyDP(contour, 0.12 * cv2.arcLength(contour, True), True)) > 3]
# # 内部の輪郭だけを取得
# internal_contours = []
# for i in range(len(contours)):
#     # 輪郭の階層構造を使用して親と子を判別
#     if hierarchy[0][i][3] != -1:
#         internal_contours.append(contours[i])

# print("\n---------------------------差分検出結果---------------------------")
# print("【 各処理後の枠数 】")
# print(f"・検出した{str_red('赤枠')}の数: {len(contours)}")
# print(f"・内部の輪郭の{str_red('赤枠')}の数: {len(internal_contours)}")

# # 面積が一定以下の輪郭を除外
# filtered_contours = filter_contours_by_area(internal_contours)
# print(f"・ノイズ除去後の{str_red('赤枠')}の数: {len(filtered_contours)}")

# # 赤枠に対して処理を行う
# for contour in filtered_contours:
#     update_text_positions(contour, text_positions)
# print(f"・近接枠結合後の{str_red('赤枠')}の数: {len(text_positions)}")

# # 枠の左上隅座標・幅・高さの情報をもつリストの作成
# for position in filtered_contours:
#     x, y, w, h = cv2.boundingRect(position)
#     correct_contours.append([x, y, x + w, y + h])

# # 赤枠を描画
# for c in correct_contours:
#     x, y, w, h = c

#     if w > 1 and h > 1:
#         # 差異が２枚目の画像で大きい場合、赤色で表示
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
#         red_rectangles.append((x, y, w, h))

# # red_rectangles の各矩形を x^2 + y^2 の和で昇順にソートする
# red_rectangles.sort(key=lambda rect: math.sqrt(rect[0]**2 + rect[1]**2))

# # 赤枠に番号を割り振りながら座標を出力
# for i, (x, y, w, h) in enumerate(red_rectangles, start=1):
#     cv2.putText(img, str(i), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
#     # print(f"赤枠{i:2}: x座標 ={x:5}, y座標 ={y:5}, 幅 ={w:4}, 高さ ={h:3}")


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

    画像内のテキストを囲む矩形を描画

"""
# OCRを実行してテキストと矩形情報を取得
result = pytesseract.image_to_data(img_gray, output_type=pytesseract.Output.DICT)

# 矩形情報を取得
boxes = zip(result['left'], result['top'], result['width'], result['height'])

# 矩形を描画
for box in boxes:
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


""" 

    後処理（差分画像を保存）

"""
### 差分画像を保存 ###
output_file_name1 = "before.png"
output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_single")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)
    command = f"sudo chown -R aridome:aridome {output_dir2}"
    # コマンドを実行
    subprocess.call(command, shell=True)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name1)

# 画像を保存する
cv2.imwrite(output_file_path, img)
# cv2.imwrite(output_file_path, img_bin_reverse)

print("------------------------------------------------------------------\n")

print(f"2つの画像の差異部分に枠をつけた画像を{output_dir2}に保存しました")
