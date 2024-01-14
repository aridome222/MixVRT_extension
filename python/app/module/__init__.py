# Pythonがディレクトリをパッケージとして扱うための特別なファイル
# このファイルが存在するディレクトリは、Pythonによってパッケージとして認識

# パッケージ全体で共有される変数や初期化コードがある場合は、ここに書く
# 使い方は、他のモジュールから from package import shared_variable, shared_function のようにして共有変数や関数を利用
# shared_variable = "This is a shared variable."

# def shared_function():
#     print("This is a shared function.")

import subprocess
import os
import glob
import shutil

# 基本ディレクトリの設定
base_dir = "python/app/base_dir"

# 差分ディレクトリの設定
diff_dir = "python/app/diff_dir"

# 表示ディレクトリの設定
images_dir = "python/app/disp/static/images"


def copy_and_rename_image(source_img, dest_dir, new_filename):
    """
    コピーして別のディレクトリに移動させたい画像をコピーし、
    指定されたデスティネーションディレクトリに新しい名前で保存します。

    :param source_img: ソース画像のパス
    :param dest_dir: 画像を保存するデスティネーションディレクトリのパス
    :param new_filename: 保存する画像の新しいファイル名
    """
    # デスティネーションディレクトリを作成し、所有者を設定
    create_dir_and_set_owner(dest_dir)

    # コピー先の新しいファイルパスを作成
    dest_img_path = os.path.join(dest_dir, new_filename)

    # 画像をコピーして名前を変更
    shutil.copy(source_img, dest_img_path)


def search_copy_and_rename_image(source_dir, dest_dir, new_filename):
    """
    指定されたソースディレクトリから画像をコピーし、
    指定されたデスティネーションディレクトリに新しい名前で保存します。

    :param source_dir: ソース画像があるディレクトリのパス
    :param dest_dir: 画像を保存するデスティネーションディレクトリのパス
    :param new_filename: 保存する画像の新しいファイル名
    """
    # デスティネーションディレクトリを作成し、所有者を設定
    create_dir_and_set_owner(dest_dir)

    # コピー元の画像のパスを取得
    source_img = get_img_path_from_dir(source_dir)

    # コピー先の新しいファイルパスを作成
    dest_img_path = os.path.join(dest_dir, new_filename)

    # 画像をコピーして名前を変更
    shutil.copy(source_img, dest_img_path)


def create_dir_and_set_owner(dir):
    """
    rootで生成されたディレクトリの権限をユーザに変更し、
    ホスト上で生成されたディレクトリ削除できるようにするための関数

    指定されたディレクトリが存在しない場合にディレクトリを作成し、
    'aridome:aridome'を所有者として設定。

    :param dir: 作成するディレクトリのパス
    """
    if not os.path.exists(dir):
        # ディレクトリを作成
        os.makedirs(dir)
        
        # 所有者を 'aridome:aridome' に設定
        command = f"sudo chown -R aridome:aridome {dir}"
        
        # コマンドを実行
        subprocess.call(command, shell=True)


def get_img_path_from_dir(dir):
    # 指定ディレクトリ内のすべての '.png' リストを取得
    img_path = glob.glob(os.path.join(dir, '**', '*.png'), recursive=True)

    # 画像が見つかった場合、最初の画像のパスを使用
    if img_path:
        first_img_path = img_path[0]
        print("Found HTML file:", first_img_path)
        return first_img_path
    else:
        print("No HTML files found in the directory.")
        return None