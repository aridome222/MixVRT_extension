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
from module import images_dir
from module import create_dir_and_set_owner


def main(diff_rec_bf_html, diff_rec_bf_img, diff_rec_af_html, diff_rec_af_img, high_img_path_of_bf_html, high_img_path_of_af_html):
    # 画像読み込み
    img_bf = cv2.imread(diff_rec_bf_img)
    html_bf = cv2.imread(diff_rec_bf_html)

    # 画像読み込み
    img_af = cv2.imread(diff_rec_af_img)
    html_af = cv2.imread(diff_rec_af_html)

    # 画像1のサイズを取得
    height1, width1 = img_bf.shape[:2]

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
    unique_contours_bf = list(contours_match_feature(contours_img_bf, contours_html_bf, (height1, width1))) + list(contours_match_feature(contours_html_bf, contours_img_bf, (height1, width1)))
    unique_contours_af = list(contours_match_feature(contours_img_af, contours_html_af, (height1, width1))) + list(contours_match_feature(contours_html_af, contours_img_af, (height1, width1)))
    # unique_contours_bf = list(contours_match(contours_img_bf, contours_html_bf)) + list(contours_match(contours_html_bf, contours_img_bf))
    # unique_contours_af = list(contours_match(contours_img_af, contours_html_af)) + list(contours_match(contours_html_af, contours_img_af))


    """ オリジナル画像の読み込み """
    # 画像読み込み
    origin_html_bf = cv2.imread(high_img_path_of_bf_html)
    origin_html_af = cv2.imread(high_img_path_of_af_html)

    bf_original = cv2.imread(os.path.join(images_dir, "original_png", "bf_original.png"))
    af_original = cv2.imread(os.path.join(images_dir, "original_png", "af_original.png"))


    """ 輪郭描画 """
    # この関数を使用して元の画像と高解像度の画像にバウンディングボックスを描画
    scale_bounding_box(bf_original, origin_html_bf, unique_contours_bf, "before", scale_to_high_res=False)
    scale_bounding_box(af_original, origin_html_af, unique_contours_af, "after", scale_to_high_res=False)
    # # 一致しない輪郭を元の画像に描画
    # for contour in unique_contours_bf:
    #     cv2.drawContours(bf_original, [contour], -1, (0, 0, 255), 5)  # 赤色で描画

    # for contour in unique_contours_af:
    #     cv2.drawContours(af_original, [contour], -1, (0, 255, 0), 5)  # 緑色で描画


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
    output_file_path_bf = os.path.join(output_dir2, output_file_name1)

    # 画像を保存する
    cv2.imwrite(output_file_path_bf, bf_original)

    # ファイルパスを作成
    output_file_path_af = os.path.join(output_dir2, output_file_name2)

    # 画像を保存する
    cv2.imwrite(output_file_path_af, af_original)


    print(f"副作用領域を検出した画像を{os.path.dirname(output_file_path_bf)}に保存しました")

    return output_file_path_bf, output_file_path_af    


def contour_to_image(contour, shape):
    # 空の画像を作成
    image = np.zeros(shape, np.uint8)
    # 輪郭を画像上に描画
    cv2.drawContours(image, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
    return image

def contours_match_feature(contour1, contour2, shape, similarity_threshold=0.5):
    # SIFTを用いた特徴点抽出器の作成
    sift = cv2.SIFT_create()

    # FLANNベースのマッチャーのパラメータ
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    unique_contours = []
    for c1 in contour1:
        match = False
        # c1輪郭を画像に変換
        c1_img = contour_to_image(c1, shape)
        kp1, des1 = sift.detectAndCompute(c1_img, None)

        for c2 in contour2:
            # c2輪郭を画像に変換
            c2_img = contour_to_image(c2, shape)
            kp2, des2 = sift.detectAndCompute(c2_img, None)

            # 特徴点が十分に存在するか確認
            if des1 is not None and des2 is not None and len(des1) >= 2 and len(des2) >= 2:
                matches = flann.knnMatch(des1, des2, k=2)

                # データセットQからデータセットTに対する良いマッチを保持
                good_matches = [m for m, n in matches if m.distance < similarity_threshold * n.distance]

                # 良いマッチが十分に存在するか確認
                if len(good_matches) > 10:
                    match = True
                    break

        if not match:
            unique_contours.append(c1)

    return unique_contours


# # 輪郭の類似度で一致か不一致かを判定
# def contours_match(contour1, contour2, similarity_threshold=0.2):
#     for c1 in contour1:
#         match = False
#         for c2 in contour2:
#             # 輪郭間の形状の類似度を計算
#             similarity = cv2.matchShapes(c1, c2, 1, 0.0)
#             if similarity < similarity_threshold:
#                 match = True
#                 break
#         if not match:
#             yield c1


# 枠の重なり度合いで一致かどうかを判定
# def contours_overlap(c1, c2):
#     # 輪郭のバウンディングボックスを取得
#     x1, y1, w1, h1 = cv2.boundingRect(c1)
#     x2, y2, w2, h2 = cv2.boundingRect(c2)

#     # バウンディングボックスが重なっているか判定
#     if not (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
#         return False

#     # 重なり部分のバウンディングボックスを計算
#     overlap_x = max(x1, x2)
#     overlap_y = max(y1, y2)
#     overlap_w = min(x1 + w1, x2 + w2) - overlap_x
#     overlap_h = min(y1 + h1, y2 + h2) - overlap_y
#     overlap_area = overlap_w * overlap_h

#     # 小さい方のバウンディングボックスの面積を計算
#     area1 = w1 * h1
#     area2 = w2 * h2
#     smaller_area = min(area1, area2)

#     # 重なりが小さい方の面積の60%以上であればTrueを返す
#     return overlap_area / smaller_area >= 0.6

# def contours_match(contour1, contour2):
#     for c1 in contour1:
#         match = False
#         for c2 in contour2:
#             if contours_overlap(c1, c2):
#                 match = True
#                 break
#         if not match:
#             yield c1


# シンプルに少しでも重なったら一致、そうでなければ不一致
# def contours_overlap(c1, c2):
#     # 輪郭のバウンディングボックスを取得
#     x1, y1, w1, h1 = cv2.boundingRect(c1)
#     x2, y2, w2, h2 = cv2.boundingRect(c2)

#     # バウンディングボックスが重なっているか判定
#     return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)


# def contours_match(contour1, contour2):
#     for c1 in contour1:
#         match = False
#         for c2 in contour2:
#             if contours_overlap(c1, c2):
#                 match = True
#                 break
#         if not match:
#             yield c1


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