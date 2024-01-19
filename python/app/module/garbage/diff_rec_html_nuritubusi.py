"""
NOTE 変更前後のhtmlからcssによる枠のみを抽出するプログラム

HTMLでコメント付きの枠に対応するためのファイル。
テキストが枠内にあるため、枠内のピクセルを黒にして枠を白くできるか検証
なぜか枠内も塗りつぶされ、失敗

"""
import cv2
import os
import numpy as np
import subprocess
import math

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def main(high_img_path_of_bf_html, high_img_path_of_modified_bf_html, high_img_path_of_af_html, high_img_path_of_modified_af_html):
    """変更前画像読み込み"""
    img1 = cv2.imread(high_img_path_of_bf_html)
    img2 = cv2.imread(high_img_path_of_modified_bf_html)

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

    """変更後画像読み込み"""
    img3 = cv2.imread(high_img_path_of_af_html)
    img4 = cv2.imread(high_img_path_of_modified_af_html)

    # 画像3のサイズを取得
    height3, width3, _ = img3.shape

    # 画像4のサイズを取得
    height4, width4, _ = img4.shape

    # ターゲットのサイズ
    target_width = 2613
    target_height = 2567

    # サイズが異なる場合はリサイズ
    if (width3, height3) != (width4, height4):
        img3 = cv2.resize(img3, (target_width, target_height))
        img4 = cv2.resize(img4, (target_width, target_height))


    """画像処理"""
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    img3_gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    img4_gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)

    # 画像の差分を計算
    diff_bf_html = cv2.absdiff(img1_gray, img2_gray)
    ret, diff_bf_html = cv2.threshold(diff_bf_html, 0, 255, cv2.THRESH_BINARY)

    diff_af_html = cv2.absdiff(img3_gray, img4_gray)
    ret, diff_af_html = cv2.threshold(diff_af_html, 0, 255, cv2.THRESH_BINARY)

    """輪郭描画"""
    # 白ピクセルを赤で塗りつぶす
    diff_bf_html_colored = cv2.cvtColor(diff_bf_html, cv2.COLOR_GRAY2BGR)
    white_pixel_indices = np.where(diff_bf_html_colored == [255, 255, 255])
    diff_bf_html_colored[white_pixel_indices[0], white_pixel_indices[1]] = [0, 0, 255]  # 白を赤に置き換え

    # 白ピクセルを緑で塗りつぶす
    diff_af_html_colored = cv2.cvtColor(diff_af_html, cv2.COLOR_GRAY2BGR)
    white_pixel_indices = np.where(diff_af_html_colored == [255, 255, 255])
    diff_af_html_colored[white_pixel_indices[0], white_pixel_indices[1]] = [0, 255, 0]  # 白を緑に置き換え


    # 輪郭抽出とフィルタリングを行う関数
    def filter_contours(diff_image, area_threshold):
        contours, _ = cv2.findContours(diff_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]
        return filtered_contours

    # 差分画像の処理
    filtered_contours_bf = filter_contours(diff_bf_html, area_threshold=100)  # area_thresholdは適宜調整
    filtered_contours_af = filter_contours(diff_af_html, area_threshold=100)  # area_thresholdは適宜調整

    # 色付きの差分画像を生成
    def create_colored_diff_image(filtered_contours, base_color):
        output_image = np.zeros_like(diff_bf_html)
        cv2.drawContours(output_image, filtered_contours, -1, (255), thickness=cv2.FILLED)
        diff_colored = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)
        white_pixel_indices = np.where(diff_colored == [255, 255, 255])
        diff_colored[white_pixel_indices[0], white_pixel_indices[1]] = base_color
        return diff_colored

    diff_bf_html_colored = create_colored_diff_image(filtered_contours_bf, [0, 0, 255])  # 赤色で塗る
    diff_af_html_colored = create_colored_diff_image(filtered_contours_af, [0, 255, 0])  # 緑色で塗る


    # 差分画像の保存
    output_dir2 = os.path.join(diff_dir, "diff_rec_html_png")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
        command = f"sudo chown -R aridome:aridome {output_dir2}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    output_file_name_bf = "diff_rec_bf_html.png"
    output_file_name_af = "diff_rec_af_html.png"

    # ファイルパスを作成
    output_file_path_bf = os.path.join(output_dir2, output_file_name_bf)
    # 画像を保存する
    cv2.imwrite(output_file_path_bf, diff_bf_html_colored)

    # ファイルパスを作成
    output_file_path_af = os.path.join(output_dir2, output_file_name_af)
    # 画像を保存する
    cv2.imwrite(output_file_path_af, diff_af_html_colored)


    print(f"HTMLコードの変更による影響箇所を囲んだ枠のみを抽出した画像を{os.path.dirname(output_file_path_bf)}に保存しました")

    return output_file_path_bf, output_file_path_af


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