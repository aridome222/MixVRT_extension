# main.pyファイル

from module.scraping import gen_modify_html_comment
from module.scraping import gen_modify_html
from module.scraping import process_get_class
from module.scraping import process
from module.scraping import test_get_after_html
from module.scraping import test_get_before_html

from module import diff_rec_img
from module import diff_rec_html
from module import gen_subEffect
from module import png_to_high_png

from module import get_html
from module import get_img


import sys


def main():
    print("----main.py is running.----")

    """ Webページの画像とHTMLを取得 """
    get_before_html.main()
    get_after_html.main()

    get_before_img.main()
    get_after_img.main()

    
    # 初回の場合の処理を書く
    

    # ２回目以降の場合の処理を書く

    """ 変更前と後のWebページのHTMLを比較する """

    """ 変更前と後のWebページの画面画像を比較する """

    """ 副作用領域を抽出する """

    """ 様々な差分画像を差分Webページに表示する """



if __name__ == "__main__":
    main()