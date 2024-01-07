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

import sys


def main():
    print("main.py is running.")

    

    # detect_rec_imgのmain関数を呼び出す
    diff_rec_img.main()


if __name__ == "__main__":
    main()