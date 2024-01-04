# main.pyファイル

from module import detect_rec_img
# from module import test_before
# from module import test_after

import sys


def main():
    print("main.py is running.")

    # # コマンドライン引数からURLを得る
    # if len(sys.argv) < 3:
    #     print("------------")
    #     print(sys.argv[0])
    #     print(sys.argv[1])
    #     # print(sys.argv[2])
    #     print("------------")
    #     print("Usage: python main.py <url1> <url2>")
    #     sys.exit(1)
        
    # url1 = sys.argv[1]
    # url2 = sys.argv[2]

    # # test_slt_addShotのmain関数を呼び出す（URL1）
    # shot1 = test_before.Test_slt_input_addShot(url1)
    # img1_path = shot1.test_singlelinetext()

    # # test_slt_addShotのmain関数を呼び出す（URL2）
    # shot2 = test_after.Test_slt_input_addShot(url2)
    # img2_path = shot2.test_singlelinetext()

    # # detect_rec_divideのmain関数を呼び出す
    # diff_img1, diff_img2 = detect_rec_divide.main(img1_path, img2_path)

    # # detect_rec_divideのmain関数を呼び出す
    # detect_rec_divide.main()

    # # detect_rec_divide_binのmain関数を呼び出す
    # detect_rec_divide_bin.main()

    # detect_rec_divide_bin2のmain関数を呼び出す
    detect_rec_img.main()

    # # detect_rec_divide_akazeのmain関数を呼び出す
    # detect_rec_divide_akaze.main()

    # return diff_img1, diff_img2

if __name__ == "__main__":
    main()