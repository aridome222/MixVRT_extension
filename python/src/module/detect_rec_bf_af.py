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
    output_file_name_A = 'bf_html2.png'
    output_file_name_B = 'af_html2.png'
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

    # clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10, 10))
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # img1_gray = clahe.apply(img1_gray)
    # img2_gray = clahe.apply(img2_gray)

    # img1_gray = cv2.GaussianBlur(img1_gray, (13, 13), 0)
    # img2_gray = cv2.GaussianBlur(img2_gray, (13, 13), 0)

    # # 画像の差分を計算
    # diff = cv2.absdiff(img1_gray, img2_gray)
    # ret, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # diff = cv2.GaussianBlur(diff, (11, 11), 0)

    ### 枠づけ ###
    # # 二値化
    # ret, img1_bin = cv2.threshold(img1_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # img1_bin = cv2.GaussianBlur(img1_bin, (11, 11), 0)
    # ret, img2_bin = cv2.threshold(img2_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # img2_bin = cv2.GaussianBlur(img2_bin, (11, 11), 0)

    img1_bin = cv2.adaptiveThreshold(img1_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                    cv2.THRESH_BINARY, 11, 2)
    img2_bin = cv2.adaptiveThreshold(img2_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                    cv2.THRESH_BINARY, 11, 2)

    # 白黒を逆にする
    img1_bin_reverse = cv2.bitwise_not(img1_bin)
    img2_bin_reverse = cv2.bitwise_not(img2_bin)

    # 画像Aから画像Bを引くことで1枚目の画像の差分のみを取得
    diff_before = cv2.subtract(img1_bin_reverse, img2_bin_reverse)
    diff_after = cv2.subtract(img2_bin_reverse, img1_bin_reverse)

    # # 形態学的な操作
    # kernel = np.ones((3,3), np.uint8)
    # diff_before = cv2.morphologyEx(diff_before, cv2.MORPH_OPEN, kernel)
    # diff_after = cv2.morphologyEx(diff_after, cv2.MORPH_OPEN, kernel)

    # 収縮・膨張処理のためのカーネルを定義
    kernel = np.ones((5,5),np.uint8)

    # 差分画像に膨張処理を適用
    diff_expanded_before = cv2.dilate(diff_before, kernel, iterations = 6)
    diff_expanded_after = cv2.dilate(diff_after, kernel, iterations = 6)

    # # 修正した差分画像を表示用にカラー変換
    # expanded_before_colored = cv2.cvtColor(diff_expanded_before, cv2.COLOR_GRAY2BGR)
    # expanded_after_colored = cv2.cvtColor(diff_expanded_after, cv2.COLOR_GRAY2BGR)

    """輪郭描画"""
    # 差分画像から輪郭抽出
    contours1, _ = cv2.findContours(diff_expanded_before, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(diff_expanded_after, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours1 = filter_contours_by_area(contours1)
    contours2 = filter_contours_by_area(contours2)


    # 元の画像に輪郭を描画する
    for contour in contours1:
        # 輪郭に囲まれた領域のバウンディングボックスを取得
        x, y, w, h = cv2.boundingRect(contour)
        # 元の画像に矩形を描画
        cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)

    for contour in contours2:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # # 二値画像に直接枠を描画
    # for contour in contours1:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # 枠を白色（255）で描画
    #     cv2.rectangle(diff_expanded_before, (x, y), (x + w, y + h), (255), 2)

    # # 二値画像に直接枠を描画
    # for contour in contours2:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # 枠を白色（255）で描画
    #     cv2.rectangle(diff_expanded_after, (x, y), (x + w, y + h), (255), 2)


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
    cv2.imwrite(output_file_path, img1)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, expanded_before_colored)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name2)

    # 画像を保存する
    cv2.imwrite(output_file_path, img2)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, expanded_after_colored)

    print(f"2つの画像の差異部分に枠をつけたカラー画像をに保存しました")


def filter_contours_by_area(contours, threshold_area=3000):
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



# __name__ が "__main__" の場合のみ実行
if __name__ == "__main__":
    main()