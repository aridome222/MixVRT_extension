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


def compare_data(url):
    print("----compare_data.py is running.----")

    """ 変更前と後のWebページのHTMLを比較する """


    """ 変更前と後のWebページの画面画像を比較する """



    """ 副作用領域を抽出する """



    """ 様々な差分画像を差分Webページに表示する """



    """ 以前実行時のcurrent_dirを新しいデータディレクトリの内容に変更 """



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebページのHTMLと画像を取得するスクリプト。')
    parser.add_argument('url', type=str, help='取得するWebページのURL。')
    args = parser.parse_args()
    compare_data(args.url)