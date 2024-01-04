"""
NOTE 変更前後のhtmlからcssによる枠のみを抽出するプログラム

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
    
    """変更前画像読み込み"""
    # ファイル名を生成
    output_file_name_A = 'bf_html2.png'
    output_file_name_B = 'noComment_bf_html2.png'
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

    """変更後画像読み込み"""
    # ファイル名を生成
    output_file_name_C = 'af_html2.png'
    output_file_name_D = 'noComment_af_html2.png'
    # ファイルパスを作成
    output_file_path_C = os.path.join(output_dir, output_file_name_C)
    output_file_path_D = os.path.join(output_dir, output_file_name_D)

    img3 = cv2.imread(output_file_path_C)
    img4 = cv2.imread(output_file_path_D)

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

    # 差分画像の保存
    output_file_name1 = "before.png"
    output_file_name2 = "after.png"
    output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_html_png")
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
        command = f"sudo chown -R aridome:aridome {output_dir2}"
        # コマンドを実行
        subprocess.call(command, shell=True)

    # # ファイルパスを作成
    # output_file_path = os.path.join(output_dir2, output_file_name1)

    # # 画像を保存する
    # cv2.imwrite(output_file_path, img1)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, expanded_before_colored)

    # # ファイルパスを作成
    # output_file_path = os.path.join(output_dir2, output_file_name2)

    # # 画像を保存する
    # cv2.imwrite(output_file_path, img2)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, expanded_after_colored)

    output_file_name_bf = "diff_bf_html.png"
    output_file_name_af = "diff_af_html.png"

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name_bf)
    # 画像を保存する
    cv2.imwrite(output_file_path, diff_bf_html)

    # ファイルパスを作成
    output_file_path = os.path.join(output_dir2, output_file_name_af)
    # 画像を保存する
    cv2.imwrite(output_file_path, diff_af_html)

    # # ファイルパスを作成
    # output_file_path = os.path.join(output_dir2, output_file_name_bf)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, result_bf)

    # # ファイルパスを作成
    # output_file_path = os.path.join(output_dir2, output_file_name_af)
    # # 画像を保存する
    # cv2.imwrite(output_file_path, result_af)


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