# 参考サイト：https://sosotata.com/spot7differences/
import cv2
import os
from datetime import datetime

# 保存先ディレクトリを作成
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_png/")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# ファイル名を生成
output_file_name_A = 'base.png'
output_file_name_B = 'chg_position.png'
# ファイルパスを作成
output_file_path_A = os.path.join(output_dir, output_file_name_A)
output_file_path_B = os.path.join(output_dir, output_file_name_B)

img1 = cv2.imread(output_file_path_A)
img2 = cv2.imread(output_file_path_B)

clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10,10))
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

# ２つの画像の差分を表示
contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 1 and h > 1:
        if img2[y:y+h, x:x+w].mean() > img1[y:y+h, x:x+w].mean():
            # 差異が２枚目の画像で大きい場合、赤色で表示
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            # 差異が１枚目の画像で大きい場合、緑色で表示
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)

# 差分画像を保存
output_file_name = f"draw_rec3_high_{output_file_name_B.split('_')[1]}"
output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_rec3_high_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, img2)

print(f"2つの画像の差異部分に枠をつけたカラー画像を{output_file_path}に保存しました")

