"""
NOTE 変更前後の画像を比較して、枠を描画＆画像比較による枠を抽出するようのプログラム

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
import shutil

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import images_dir
from module import create_dir_and_set_owner
from module import copy_and_rename_image


def main(high_img_path_of_bf_html, high_img_path_of_af_html):
    img1 = cv2.imread(high_img_path_of_bf_html)
    img2 = cv2.imread(high_img_path_of_af_html)

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

    # 収縮・膨張処理のためのカーネルを定義
    kernel = np.ones((5,5),np.uint8)

    # 差分画像に膨張処理を適用
    diff_expanded_before = cv2.dilate(diff_before, kernel, iterations = 6)
    diff_expanded_after = cv2.dilate(diff_after, kernel, iterations = 6)


    """輪郭描画"""
    # 差分画像から輪郭抽出
    contours1, _ = cv2.findContours(diff_expanded_before, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(diff_expanded_after, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours1 = filter_contours_by_area(contours1)
    contours2 = filter_contours_by_area(contours2)

    bf_original = cv2.imread(os.path.join(images_dir, "original_png", "bf_original.png"))
    af_original = cv2.imread(os.path.join(images_dir, "original_png", "af_original.png"))

    # この関数を使用して元の画像と高解像度の画像にバウンディングボックスを描画
    scale_bounding_box(bf_original, img1, contours1, "before", scale_to_high_res=False)
    scale_bounding_box(af_original, img2, contours2, "after", scale_to_high_res=False)


    # # 元の画像に輪郭を描画する
    # for contour in contours1:
    #     # 輪郭に囲まれた領域のバウンディングボックスを取得
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # 元の画像に矩形を描画
    #     cv2.rectangle(bf_original, (x, y), (x + w, y + h), (0, 0, 255), 5)

    # for contour in contours2:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(af_original, (x, y), (x + w, y + h), (0, 255, 0), 5)


    # 画像のサイズを取得
    height, width = img1.shape[:2]

    # 同じサイズの黒画像を生成
    contour1_image = np.zeros((height, width, 3), dtype=np.uint8)
    contour2_image = np.zeros((height, width, 3), dtype=np.uint8)

    # 輪郭のみの画像を描画する
    for contour in contours1:
        # 輪郭に囲まれた領域のバウンディングボックスを取得
        x, y, w, h = cv2.boundingRect(contour)
        # 元の画像に矩形を描画
        cv2.rectangle(contour1_image, (x, y), (x + w, y + h), (0, 0, 255), 5)

    for contour in contours2:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(contour2_image, (x, y), (x + w, y + h), (0, 255, 0), 5)


    # 差分画像の保存
    output_file_name_bf_img = "diff_bf_img.png"
    output_file_name_af_img = "diff_af_img.png"
    output_dir = os.path.join(diff_dir, "diff_rec_img_png")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        command = f"sudo chown -R aridome:aridome {output_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # ファイルパスを作成
    output_file_path_bf_img = os.path.join(output_dir, output_file_name_bf_img)

    # 画像を保存する
    cv2.imwrite(output_file_path_bf_img, bf_original)
    # 差分箇所に枠を付けた変更前画像をapp/disp/static/images/diff_img_pngに保存
    dest_dir = os.path.join(images_dir, "diff_img_png")
    copy_and_rename_image(output_file_path_bf_img, dest_dir, output_file_name_bf_img)

    # ファイルパスを作成
    output_file_path_af_img = os.path.join(output_dir, output_file_name_af_img)

    # 画像を保存する
    cv2.imwrite(output_file_path_af_img, af_original)
    # 差分箇所に枠を付けた変更後画像をapp/disp/static/images/diff_img_pngに保存
    copy_and_rename_image(output_file_path_af_img, dest_dir, output_file_name_af_img)


    output_file_name_bf_rec_img = "diff_rec_bf_img.png"
    output_file_name_af_rec_img = "diff_rec_af_img.png"
    # ファイルパスを作成
    output_file_path_bf_rec_img = os.path.join(output_dir, output_file_name_bf_rec_img)
    # 画像を保存する
    cv2.imwrite(output_file_path_bf_rec_img, contour1_image)

    # ファイルパスを作成
    output_file_path_af_rec_img = os.path.join(output_dir, output_file_name_af_rec_img)
    # 画像を保存する
    cv2.imwrite(output_file_path_af_rec_img, contour2_image)


    print(f"2つの画像の差異部分に枠をつけたカラー画像をに保存しました")

    return output_file_path_bf_rec_img, output_file_path_af_rec_img


def scale_bounding_box(orig_img, high_res_img, contours, bf_or_af, scale_to_high_res=True):
    # 画像の解像度を取得
    orig_height, orig_width = orig_img.shape[:2]
    high_res_height, high_res_width = high_res_img.shape[:2]

    # 解像度の比率を計算
    width_ratio = high_res_width / orig_width
    height_ratio = high_res_height / orig_height

    # 輪郭に対して処理を行う
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # スケーリングする必要がある場合、バウンディングボックスをスケーリング
        if scale_to_high_res:
            x = int(x * width_ratio)
            y = int(y * height_ratio)
            w = int(w * width_ratio)
            h = int(h * height_ratio)
            if bf_or_af == "before":
                cv2.rectangle(high_res_img, (x, y), (x + w, y + h), (0, 0, 255), 5)
            else:
                cv2.rectangle(high_res_img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        else:
            x = int(x / width_ratio)
            y = int(y / height_ratio)
            w = int(w / width_ratio)
            h = int(h / height_ratio)
            if bf_or_af == "before":
                cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0, 0, 255), 5)
            else:
                cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0, 255, 0), 5)


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