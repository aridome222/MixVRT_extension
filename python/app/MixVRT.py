"""
@author: aridome222
作成日: 2024/01/10
更新日: 2024/05/05


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
    MixVRT.pyを実行する。
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
import time

# module 内の __init__.py から関数をインポート
from module import base_dir # base_dir = "python/app/base_dir"
from module import diff_dir # diff_dir = "python/app/diff_dir"
from module import images_dir # images_dir = "python/app/disp/static/images"
from module import get_img_path_from_dir
from module import create_dir_and_set_owner
from module import search_copy_and_rename_image

# その他module内の関数をインポート
from module.get_html_and_img import main as get_html_and_img_main
from module.compare_data import compare_data


def main(url):
    print("----main.py is running.----")

    # 処理開始時間を記録
    start_time = time.time()

    """ ディレクトリパス等の設定 """  
    # 基本ディレクトリの生成
    create_dir_and_set_owner(base_dir)
    # 初期データを保存するディレクトリパスの設定
    initial_dir = os.path.join(base_dir, "initial")
    # 現在のデータを保存するディレクトリパスの設定
    current_dir = os.path.join(base_dir, "current")
    # 現在の日時に基づいたタイムスタンプを生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 新しいデータを保存するディレクトリのパスを生成
    new_data_dir = os.path.join(base_dir, timestamp)
    # 差分ディレクトリの生成
    create_dir_and_set_owner(diff_dir)

    
    """ Webページの画像とHTMLを取得 """
    ### 初回実行の確認 ###
    if not os.path.exists(initial_dir):
        # 初期ディレクトリとcurrentディレクトリを作成
        create_dir_and_set_owner(initial_dir)
        if os.path.exists(current_dir):
            shutil.rmtree(current_dir)
        create_dir_and_set_owner(current_dir)
        # 指定したURLからHTMLと画像を取得し、初期ディレクトリに保存
        get_html_and_img_main(initial_dir, url)
        try:
            shutil.copytree(initial_dir, current_dir, dirs_exist_ok=True)  # Python 3.8 以降の場合
        except Exception as e:
            print(f"Error during copying: {e}")

        # 初回実行時のオリジナル画像をapp/disp/static/images/original_png/に保存
        # current_dir下にある画像を宛先のディレクトリに任意の名前でコピー
        dest_dir = os.path.join(images_dir, "original_png")
        search_copy_and_rename_image(current_dir, dest_dir, "bf_original.png")

        # 初回実行時はここで処理を"終了"
        print("初回実行は正常に終了しました")
        return
    
    
    ### ２回目以降の実行時の処理 ###
    # 新しいディレクトリを作成
    create_dir_and_set_owner(new_data_dir)
    # 指定したURLからHTMLと画像を取得し、新しいディレクトリに保存
    get_html_and_img_main(new_data_dir, url)


    """ これから比較する変更前後のオリジナル画像をapp/disp/static/images/original_pngに保存 """
    # 変更前後のオリジナル画像をapp/disp/static/images/original_png/に保存
    # current_dir下にある画像を宛先のディレクトリに任意の名前でコピー
    dest_dir = os.path.join(images_dir, "original_png")
    search_copy_and_rename_image(current_dir, dest_dir, "bf_original.png")
    search_copy_and_rename_image(new_data_dir, dest_dir, "af_original.png")


    """ 変更前後のWebページにおける画像とHTMLの比較 """
    # currentディレクトリと新しいデータディレクトリの内容を比較
    compare_data(current_dir, new_data_dir)


    """ 以前実行時のcurrent_dirを新しいデータディレクトリの内容に変更 """
    # 現在のデータを保存するディレクトリパスの設定
    latest_dir = os.path.join(base_dir, "latest")
    create_dir_and_set_owner(latest_dir)

    # currentディレクトリがすでに存在する場合は削除
    if os.path.exists(latest_dir):
        shutil.rmtree(latest_dir)
    # 新しいデータディレクトリの内容をcurrentディレクトリにコピー
    shutil.copytree(new_data_dir, latest_dir)
    command = f"sudo chown -R aridome:aridome {latest_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)

    # 処理終了時間を記録
    end_time = time.time()

    # 処理時間を計算して表示
    execution_time = end_time - start_time
    print("処理時間：", execution_time, "秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebページのHTMLと画像を取得するスクリプト。')
    parser.add_argument('url', type=str, help='取得するWebページのURL。')
    args = parser.parse_args()
    if args.url.startswith("http://localhost"):
        url = args.url.replace("http://localhost", "http://host.docker.internal")
    else:
        url = args.url
    main(url)