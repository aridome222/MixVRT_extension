# main.pyファイル

from module import detect_rec_divide
from module import detect_rec_divide_bin
from module import detect_rec_divide_akaze


def main():
    print("main.py is running.")

    # detect_rec_divideのmain関数を呼び出す
    detect_rec_divide.main()

    # # detect_rec_divide_binのmain関数を呼び出す
    # detect_rec_divide_bin.main()

    # # detect_rec_divide_akazeのmain関数を呼び出す
    # detect_rec_divide_akaze.main()


if __name__ == "__main__":
    main()