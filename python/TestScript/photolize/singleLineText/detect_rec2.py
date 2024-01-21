# 参考サイト：https://gazushige.com/blog/319668e7-c5ac-470c-a28e-f01214e69a8a
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
img1 = cv2.imread(output_file_path_A, cv2.COLOR_BGR2GRAY)
img2 = cv2.imread(output_file_path_B, cv2.COLOR_BGR2GRAY)

# Convert images to grayscale
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Resize images to the same size
height, width = img2.shape[:2] # img2のサイズを取得
img1_gray = cv2.resize(img1_gray, (width, height)) # img1をimg2と同じサイズにリサイズ

# Calculate absolute difference between the two images
diff = cv2.absdiff(img1_gray, img2_gray)

# Apply threshold to identify significant differences
thresh = 30
diff[diff < thresh] = 0
diff[diff >= thresh] = 255

# Find contours of significant differences
contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw rectangles around the differences
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

# # 現在の日付を取得してフォーマット
# current_date = datetime.now().strftime("%m-%d_%H-%M-%S")

output_file_name = f"draw_rec2_high_{output_file_name_B.split('_')[1]}"

output_dir2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_rec2_high_png")
# フォルダが存在しない場合は作成
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)

# ファイルパスを作成
output_file_path = os.path.join(output_dir2, output_file_name)

# 画像を保存する
cv2.imwrite(output_file_path, img2)

print(f"2つの画像の差異部分に枠をつけた画像を{output_file_path}に保存しました")