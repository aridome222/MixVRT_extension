"""
NOTE 差分領域の検出ができているかを確認するようのプログラム

本プログラムの機能
    2つの入力画像の差分を追加部分と削除部分に分けた画像を出力

入力画像は、以下を想定。
    ・WebアプリやWebページをスクリーンショットした画面画像
    ・背景が白地
    ・画面要素の「追加・削除・移動・変更・拡縮」の基本的な変更のみ
を想定

主な処理は、画像処理により以下を生成
    ・削除された部分が白、その他の部分が黒の画像A
    ・追加された部分が白、その他の部分が黒の画像B
その後、上記の画像の白を囲む矩形領域の座標を取得し、
    ・画像Aに矩形領域を赤枠
    ・画像Bに矩形領域を緑枠
で描画した2つの画像を出力
    

参考サイト
    https://sosotata.com/spot7differences/

"""
import cv2
import os
import numpy as np
import subprocess
import math

def main():
    # 保存先ディレクトリを作成
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # ファイル名を生成
    output_file_name_A = 'bf_html.png'
    output_file_name_B = 'af_html.png'
    # ファイルパスを作成
    output_file_path_A = os.path.join(output_dir, output_file_name_A)
    output_file_path_B = os.path.join(output_dir, output_file_name_B)

    img1 = cv2.imread(output_file_path_A)
    img2 = cv2.imread(output_file_path_B)

    # 画像1のサイズを取得
    height1, width1, _ = img1.shape

    # 画像2のサイズを取得
    height2, width2, _ = img2.shape

    # ターゲットのサイズ
    target_width = 2613
    target_height = 2567

    # サイズが異なる場合はリサイズ
    if (width1, height1) != (width2, height2):
        img1 = cv2.resize(img1, (target_width, target_height))
        img2 = cv2.resize(img2, (target_width, target_height))

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

    # 膨張処理のためのカーネルを定義
    kernel = np.ones((5,5),np.uint8)

    # 差分画像に膨張処理を適用
    diff_expanded_before = cv2.dilate(diff_before, kernel, iterations = 5)
    diff_expanded_after = cv2.dilate(diff_after, kernel, iterations = 5)

    # 修正した差分画像を表示用にカラー変換
    expanded_before_colored = cv2.cvtColor(diff_expanded_before, cv2.COLOR_GRAY2BGR)
    expanded_after_colored = cv2.cvtColor(diff_expanded_after, cv2.COLOR_GRAY2BGR)

    """輪郭描画"""
    # 差分画像に輪郭を描画
    contours1, _ = cv2.findContours(diff_expanded_before, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(diff_expanded_after, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

    # 原画像をカラーに変換
    before = cv2.cvtColor(diff_expanded_before, cv2.COLOR_GRAY2BGR)
    # 原画像をカラーに変換
    after = cv2.cvtColor(diff_expanded_after, cv2.COLOR_GRAY2BGR)

    # 枠を描画
    for c in correct_contours1:
        x, y, w, h = c

        if w > 1 and h > 1:
            # 差異が２枚目の画像で大きい場合、赤色で表示
            cv2.rectangle(before, (x, y), (x + w, y + h), (0, 0, 255), 3)
            red_rectangles.append((x, y, w, h))

    # 枠を描画
    for c in correct_contours2:
        x, y, w, h = c

        if w > 1 and h > 1:
            # 差異が１枚目の画像で大きい場合、緑色で表示
            cv2.rectangle(after, (x, y), (x + w, y + h), (0, 255, 0), 4)
            green_rectangles.append((x, y, w, h))


    # 差分画像の保存
    output_file_name1 = "before.png"
    output_file_name2 = "after.png"
    output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_png")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name1)

    # 画像を保存する
    cv2.imwrite(output_file_path, diff_expanded_before)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name2)

    # 画像を保存する
    cv2.imwrite(output_file_path, diff_expanded_after)

    print(f"2つの画像の差異部分に枠をつけたカラー画像をに保存しました")


# __name__ が "__main__" の場合のみ実行
if __name__ == "__main__":
    main()