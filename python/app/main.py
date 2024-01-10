"""

試作ツール【MixVRT】のメイン処理

入力: WebページのURL（main.py実行時にユーザがCLI上で引数として入力）
出力: 差分確認ビュー画面（web上に公開）

*** ただし、入力とするURLのWebページのHTMLは、静的なページであり、
    styleタグ内またはstyle属性にページのスタイル情報が書かれているものとする。
    また、赤や緑の色が使われておらず、基本的に白と黒で配色されるページとする。

主な処理の流れ:
    初回実行時:
        Webページの画像とHTMLを取得して終了
    ２回目以降実行時:
        1. Webページの画像とHTMLを取得
        2. 変更前後のWebページにおける画像とHTMLの比較
        3. 差分画像を差分Webページ上に公開

使い方:
    Webページ開発において、
    視覚的回帰テストを行いたい、webページのURLを引数として、
    main.pyを実行する。
    ただし、初回実行時は比較対象となるデータが存在せず視覚的回帰テストを行えないため、
    ２回目以降実行時から視覚的回帰テストを行う。
    視覚的回帰テストによって生成した差分画像を確認するには、
    指定の差分Webページ上にアクセスし、
    差分画像を見てレイアウトの不具合が発生していないかどうかを確認できる。

"""
import os
import shutil
import datetime
import subprocess
import argparse

# module 内の __init__.py から関数をインポート
from module import create_dir_and_set_owner

# その他module内の関数をインポート
from module.get_html_and_img import main as get_html_and_img_main
from module import compare_data


def main(url):
    print("----main.py is running.----")

    """ 保存するディレクトリパス等の設定 """  
    # 基本ディレクトリの設定
    base_dir = "python/app/base_dir"
    create_dir_and_set_owner(base_dir)
    # 現在のデータを保存するディレクトリのパスを生成
    current_dir = os.path.join(base_dir, "current")
    # 現在の日時に基づいたタイムスタンプを生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    """ Webページの画像とHTMLを取得 """
    # currentディレクトリが存在しない場合（初回実行時）
    if not os.path.exists(current_dir):
        # currentディレクトリを作成
        os.makedirs(current_dir)
        command = f"sudo chown -R aridome:aridome {current_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)
        # 指定したURLからHTMLと画像を取得し、currentディレクトリに保存
        get_html_and_img_main(current_dir, url)
        # 初回実行の場合はここで処理を"終了"
        return
    

    # 新しいデータを保存するディレクトリのパスを生成（２回目以降実行時）
    new_data_dir = os.path.join(base_dir, timestamp)
    # 新しいディレクトリを作成
    create_dir_and_set_owner(new_data_dir)
    # 指定したURLからHTMLと画像を取得し、新しいディレクトリに保存
    get_html_and_img_main(new_data_dir, url)


    """ 変更前後のWebページにおける画像とHTMLの比較 """
    # currentディレクトリと新しいデータディレクトリの内容を比較
    compare_data(current_dir, new_data_dir)


    """ 様々な差分画像を差分Webページに表示する """
    # display_diff()


    """ 以前実行時のcurrent_dirを新しいデータディレクトリの内容に変更 """
    # currentディレクトリがすでに存在する場合は削除
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)
    # 新しいデータディレクトリの内容をcurrentディレクトリにコピー
    shutil.copytree(new_data_dir, current_dir)
    command = f"sudo chown -R aridome:aridome {current_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebページのHTMLと画像を取得するスクリプト。')
    parser.add_argument('url', type=str, help='取得するWebページのURL。')
    args = parser.parse_args()
    main(args.url)