# Pythonがディレクトリをパッケージとして扱うための特別なファイル
# このファイルが存在するディレクトリは、Pythonによってパッケージとして認識

# パッケージ全体で共有される変数や初期化コードがある場合は、ここに書く
# 使い方は、他のモジュールから from package import shared_variable, shared_function のようにして共有変数や関数を利用
# shared_variable = "This is a shared variable."

# def shared_function():
#     print("This is a shared function.")
