# 成功作（2つの画像を比較して、枠内で差分があるかどうかを判定）
# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
import numpy as np
import subprocess


class DetectInputRect:
    def __init__(self, img) -> None:
        self.img = img

    def get_input_rect_info(self) -> :
        # 保存先ディレクトリを作成
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
        # フォルダが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            command = f"sudo chown -R aridome:aridome {output_dir}"
            # コマンドを実行
            subprocess.call(command, shell=True)

        # ファイル名を生成
        output_file_name_A = self.img
        # ファイルパスを作成
        output_file_path_A = os.path.join(output_dir, output_file_name_A)

        img1 = cv2.imread(output_file_path_A)

        # BGRからHSVに変換
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

        # 薄水色のHSVの範囲# [色相, 彩度, 明度]
        hsv_min = np.array([90, 3, 0]) 
        hsv_max = np.array([110, 20, 255])

        # マスク画像を作成
        mask = cv2.inRange(hsv, hsv_min, hsv_max)

        # マスクされた画像を作成
        masked_img1 = cv2.bitwise_and(img1, img1, mask=mask)

        # カラー画像をグレースケール画像に変換
        masked_img1_gray = cv2.cvtColor(masked_img1, cv2.COLOR_BGR2GRAY)

        # マスク画像から白い領域の輪郭を検出する
        contours, hierarchy = cv2.findContours(masked_img1_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        selected_contours = []
        for cnt in contours:
            if cv2.contourArea(cnt)>1000: #数字は試行錯誤が必要
                epsilon = 0.01*cv2.arcLength(cnt,True) #数字は試行錯誤が必要
                approx = cv2.approxPolyDP(cnt,epsilon,True)
                selected_contours.append(approx)

        # 別の画像に輪郭を描画する
        # result = np.zeros_like(img1)
        cv2.drawContours(img1, selected_contours, -1, color=255, thickness=2)

        # 輪郭に番号を付ける
        font = cv2.FONT_HERSHEY_SIMPLEX # フォントの種類
        font_size = 0.5 # フォントのサイズ
        font_color = (0, 0, 255) # フォントの色（BGR）
        for i, cnt in enumerate(selected_contours):
            x, y, w, h = cv2.boundingRect(cnt) # 矩形領域の座標と幅と高さを取得
            cv2.putText(img1, str(i+1), (x+w//2, y+h//2), font, font_size, font_color) # 矩形領域の中心に番号を描画

        # 輪郭から矩形領域の座標情報を取得する
        rectangles = []
        for cnt in selected_contours:
            x, y, w, h = cv2.boundingRect(cnt) # x, yは左上の座標、w, hは幅と高さ
            rectangles.append((x, y, w, h))

        # 矩形領域の数をカウント
        num_rectangles = len(rectangles)
        print(f"＜入力欄の数＞: {num_rectangles}個\n")

        # 矩形領域の座標情報をひとつずつ表示する
        for i, rect in enumerate(rectangles):
            print(f"入力欄{i+1}の座標: ({rect[0]}, {rect[1]})")
            print(f"入力欄{i+1}の幅: {rect[2]}")
            print(f"入力欄{i+1}の高さ: {rect[3]}")
            print()

        # 差分画像を保存
        if output_file_name_A == "base.png":
            output_file_name = f"judge_high_{output_file_name_A}"
        else:
            output_file_name = f"judge_high_{output_file_name_A.split('_')[1]}"
        output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_high_png")
        # フォルダが存在しない場合は作成
        if not os.path.exists(output_dir2):
            os.makedirs(output_dir2)
            command = f"sudo chown -R aridome:aridome {output_dir2}"
            # コマンドを実行
            subprocess.call(command, shell=True)

        # ファイルパスを作成
        output_file_path = os.path.join(output_dir2, output_file_name)

        # 画像を保存する
        cv2.imwrite(output_file_path, img1)

        print(f"2つの画像の差異部分に枠をつけたカラー画像を{output_file_path}に保存しました")
