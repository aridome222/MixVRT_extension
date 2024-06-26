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
img1 = cv2.imread(output_file_path_A, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(output_file_path_B, cv2.IMREAD_GRAYSCALE)

clahe = cv2.createCLAHE(clipLimit=30.0, tileGridSize=(10,10))
img1 = clahe.apply(img1)
img2 = clahe.apply(img2)

img1 = cv2.GaussianBlur(img1,(13,13),0) # GaussianBlurのパラメータは適宜調整
img2 = cv2.GaussianBlur(img2,(13,13),0) # GaussianBlurのパラメータは適宜調整

diff = cv2.absdiff(img1, img2)
ret, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
diff = cv2.GaussianBlur(diff,(11,11),0) # GaussianBlurのパラメータは適宜調整

img2 = cv2.imread(output_file_path_B)
contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w > 1 and h > 1: # ゴミ検出を除去するために15 x 15未満の小さい領域を対象外とする
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 3)

# # 現在の日付を取得してフォーマット
# current_date = datetime.now().strftime("%m-%d_%H-%M-%S")

output_file_name = f"draw_rec_high_{output_file_name_B.split('_')[1]}"

output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_rec_high_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, img2)

print(f"2つの画像の差異部分に枠をつけた画像を{output_file_path}に保存しました")