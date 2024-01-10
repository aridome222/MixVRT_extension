# Pythonがディレクトリをパッケージとして扱うための特別なファイル
# このファイルが存在するディレクトリは、Pythonによってパッケージとして認識

# パッケージ全体で共有される変数や初期化コードがある場合は、ここに書く
# 使い方は、他のモジュールから from package import shared_variable, shared_function のようにして共有変数や関数を利用
# shared_variable = "This is a shared variable."

# def shared_function():
#     print("This is a shared function.")

import subprocess
import os


def create_dir_and_set_owner(dir):
    """
    rootで生成されたディレクトリの権限をユーザに変更し、
    ホスト上で生成されたディレクトリ削除できるようにするための関数

    指定されたディレクトリが存在しない場合にディレクトリを作成し、
    'aridome:aridome'を所有者として設定。

    :param base_dir: 作成するディレクトリのパス
    """
    if not os.path.exists(dir):
        # ディレクトリを作成
        os.makedirs(dir)
        
        # 所有者を 'aridome:aridome' に設定
        command = f"sudo chown -R aridome:aridome {dir}"
        
        # コマンドを実行
        subprocess.call(command, shell=True)
