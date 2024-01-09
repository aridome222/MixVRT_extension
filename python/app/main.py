# main.pyファイル

# from module.scraping import gen_modify_html_comment
# from module.scraping import gen_modify_html
# from module.scraping import process_get_class
# from module.scraping import process
# from module.scraping import test_get_after_html
# from module.scraping import test_get_before_html

from module import gen_subEffect
# from module import png_to_high_png


from module.get_html_and_img import main as get_html_and_img_main


import os
import shutil
import datetime
import subprocess
import argparse


def main(url):
    print("----main.py is running.----")

    """ Webページの画像とHTMLを取得 """
    # 基本ディレクトリの設定
    base_dir = "python/app/log_dir"
    # 現在のデータを保存するディレクトリのパスを生成
    current_dir = os.path.join(base_dir, "current")
    # 現在の日時に基づいたタイムスタンプを生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # currentディレクトリが存在しない場合（初回実行時）
    if not os.path.exists(current_dir):
        # currentディレクトリを作成
        os.makedirs(current_dir)
        command = f"sudo chown -R aridome:aridome {current_dir}"
        # コマンドを実行
        subprocess.call(command, shell=True)
        # 指定したURLからHTMLと画像を取得し、currentディレクトリに保存
        get_html_and_img_main(current_dir, url)
        # 初回実行の場合はここで処理を終了
        return
    

    # 新たなHTMLと画像を取得し、タイムスタンプ付きディレクトリに保存（２回目以降実行時）
    # 新しいデータを保存するディレクトリのパスを生成
    new_data_dir = os.path.join(base_dir, timestamp)
    # 新しいディレクトリを作成
    os.makedirs(new_data_dir)
    command = f"sudo chown -R aridome:aridome {current_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)
    # 指定したURLからHTMLと画像を取得し、新しいディレクトリに保存
    get_html_and_img_main(new_data_dir, url)


    """ 変更前と後のWebページのHTMLを比較する """
    # currentディレクトリと新しいデータディレクトリの内容を比較
    # compare_data(current_dir, new_data_dir)


    """ 変更前と後のWebページの画面画像を比較する """



    """ 副作用領域を抽出する """



    """ 様々な差分画像を差分Webページに表示する """



    """ 以前実行時のcurrent_dirを新しいデータディレクトリの内容に変更 """

    # currentディレクトリがすでに存在する場合は削除
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)
    # 新しいデータディレクトリの内容をcurrentディレクトリにコピー
    shutil.copytree(new_data_dir, current_dir)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebページのHTMLと画像を取得するスクリプト。')
    parser.add_argument('url', type=str, help='取得するWebページのURL。')
    args = parser.parse_args()
    main(args.url)