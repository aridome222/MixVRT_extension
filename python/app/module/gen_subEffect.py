"""
NOTE 画像の枠とhtmlの枠を比較して副作用領域を求め、
    元画像に副作用領域を描画した画像を生成する

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

# module 内の __init__.py から関数をインポート
from module import base_dir
from module import diff_dir
from module import create_dir_and_set_owner


def main(diff_rec_bf_html, diff_rec_bf_img, diff_rec_af_html, diff_rec_af_img, high_img_path_of_bf_html, high_img_path_of_af_html):
    # 画像読み込み
    img_bf = cv2.imread(diff_rec_bf_img)
    html_bf = cv2.imread(diff_rec_bf_html)

    # 画像読み込み
    img_af = cv2.imread(diff_rec_af_img)
    html_af = cv2.imread(diff_rec_af_html)

    # # 画像1のサイズを取得
    # height1, width1, _ = img1.shape

    # # 画像2のサイズを取得
    # height2, width2, _ = img2.shape

    # # ターゲットのサイズ
    # target_width = 2613
    # target_height = 2567

    # # サイズが異なる場合はリサイズ
    # if (width1, height1) != (width2, height2):
    #     img1 = cv2.resize(img1, (target_width, target_height))
    #     img2 = cv2.resize(img2, (target_width, target_height))

    img_bf_gray = cv2.cvtColor(img_bf, cv2.COLOR_BGR2GRAY)
    html_bf_gray = cv2.cvtColor(html_bf, cv2.COLOR_BGR2GRAY)
    img_af_gray = cv2.cvtColor(img_af, cv2.COLOR_BGR2GRAY)
    html_af_gray = cv2.cvtColor(html_af, cv2.COLOR_BGR2GRAY)

    ret, img_bf_bin = cv2.threshold(img_bf_gray, 0, 255, cv2.THRESH_BINARY)
    ret, html_bf_bin = cv2.threshold(html_bf_gray, 0, 255, cv2.THRESH_BINARY)
    ret, img_af_bin = cv2.threshold(img_af_gray, 0, 255, cv2.THRESH_BINARY)
    ret, html_af_bin = cv2.threshold(html_af_gray, 0, 255, cv2.THRESH_BINARY)


    """ 副作用領域の検出 """    
    # 差分画像から輪郭抽出
    contours_img_bf, _ = cv2.findContours(img_bf_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_html_bf, _ = cv2.findContours(html_bf_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_img_af, _ = cv2.findContours(img_af_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_html_af, _ = cv2.findContours(html_af_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # contours1 = filter_contours_by_area(contours1)
    # contours2 = filter_contours_by_area(contours2)

    # 一致しない輪郭を探す
    unique_contours_bf = list(contours_match(contours_img_bf, contours_html_bf)) + list(contours_match(contours_html_bf, contours_img_bf))
    unique_contours_af = list(contours_match(contours_img_af, contours_html_af)) + list(contours_match(contours_html_af, contours_img_af))


    """ オリジナル画像の読み込み """
    # 画像読み込み
    origin_html_bf = cv2.imread(high_img_path_of_bf_html)
    origin_html_af = cv2.imread(high_img_path_of_af_html)


    """ 輪郭描画 """
    # 一致しない輪郭を元の画像に描画
    for contour in unique_contours_bf:
        cv2.drawContours(origin_html_bf, [contour], -1, (0, 0, 255), 5)  # 赤色で描画

    for contour in unique_contours_af:
        cv2.drawContours(origin_html_af, [contour], -1, (0, 255, 0), 5)  # 緑色で描画


    """ 副作用領域を描画した画像の生成 """
    # 差分画像の保存
    output_file_name1 = "subEffect_bf.png"
    output_file_name2 = "subEffect_af.png"
    output_dir2 = os.path.join(diff_dir, "sub_effect_png")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
        command = f"sudo chown -R aridome:aridome {output_dir2}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name1)

    # 画像を保存する
    cv2.imwrite(output_file_path, origin_html_bf)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name2)

    # 画像を保存する
    cv2.imwrite(output_file_path, origin_html_af)


    print(f"副作用領域を検出した画像を{os.path.dirname(output_file_path)}に保存しました")


def contours_overlap(c1, c2):
    # 輪郭のバウンディングボックスを取得
    x1, y1, w1, h1 = cv2.boundingRect(c1)
    x2, y2, w2, h2 = cv2.boundingRect(c2)

    # バウンディングボックスが重なっているか判定
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)


def contours_match(contour1, contour2):
    for c1 in contour1:
        match = False
        for c2 in contour2:
            if contours_overlap(c1, c2):
                match = True
                break
        if not match:
            yield c1


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