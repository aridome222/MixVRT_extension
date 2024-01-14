"""
@author: aridome222
作成日: 2024/01/10
更新日: 2024/01/10


試作ツール【MixVRT】の機能であるWebページの画像とHTMLの比較処理

"""
import os
import shutil
import datetime
import subprocess
import argparse
import glob

# module 内の __init__.py から関数をインポート
from module import images_dir # images_dir = "python/app/disp/static/images"
from module import create_dir_and_set_owner
from module import get_img_path_from_dir
from module import copy_and_rename_image

# その他module内の関数をインポート
from module import png_to_high_png
from module import gen_subEffect

from module.diff_html import process
from module.diff_html import gen_modify_html
from module.diff_html import diff_rec_html

from module.diff_img import diff_rec_img

from module.get_html_or_img import get_img


def compare_data(current_dir, new_data_dir):
    print("----compare_data.py is running.----")

    """ 変更前と後のWebページの画面画像を比較する """
    # 変更前後のWebページの画像を高画質にした画像を生成
    high_img_path_of_bf_html = png_to_high_png.png_to_high_png(get_img_path_from_dir(current_dir))
    high_img_path_of_af_html = png_to_high_png.png_to_high_png(get_img_path_from_dir(new_data_dir))
    # 画像比較に基づく差分箇所を囲んだ枠のみを抽出した画像を生成
    diff_rec_bf_img, diff_rec_af_img = diff_rec_img.main(high_img_path_of_bf_html, high_img_path_of_af_html)


    """ 変更前と後のWebページのHTMLを比較する """
    # 枠付け処理を行った変更前後のWebページを開発環境で表示するためのURL
    modified_bf_url = "http://host.docker.internal:5000/modified_testPage_bf"
    modified_af_url = "http://host.docker.internal:5000/modified_testPage_af"

    # 変更前後のHTMLを比較して差分ファイルを生成
    diff_html_file_path = process.gen_diff_html(current_dir, new_data_dir)
    # 差分ファイルから元の変更前後のHTMLに枠付け処理をしたHTMLを生成
    modified_before_file_path, modified_after_file_path = gen_modify_html.main(diff_html_file_path)
    # 枠付け処理をした変更前後のWebページの画像を取得
    img_path_of_modified_bf_html = get_img.main(modified_bf_url, modified_before_file_path)
    img_path_of_modified_af_html = get_img.main(modified_af_url, modified_after_file_path)
    # 枠づけ処理をした変更前後のWebページ画像をapp/disp/static/images/diff_html_pngに保存
    dest_dir = os.path.join(images_dir, "diff_html_png")
    copy_and_rename_image(img_path_of_modified_bf_html, dest_dir, "diff_bf_html.png")
    copy_and_rename_image(img_path_of_modified_af_html, dest_dir, "diff_af_html.png")
    # 枠付け処理をした変更前後のWebページの画像を高画質にした画像を生成
    high_img_path_of_modified_bf_html = png_to_high_png.png_to_high_png(img_path_of_modified_bf_html)
    high_img_path_of_modified_af_html = png_to_high_png.png_to_high_png(img_path_of_modified_af_html)
    # HTMLコードの変更による影響箇所を囲んだ枠のみを抽出した画像を生成
    diff_rec_bf_html, diff_rec_af_html = diff_rec_html.main(high_img_path_of_bf_html, high_img_path_of_modified_bf_html, high_img_path_of_af_html, high_img_path_of_modified_af_html)


    """ 副作用領域を抽出する """
    # 抽出した副作用領域を描画した画像を生成
    subEffect_bf, subEffect_af = gen_subEffect.main(diff_rec_bf_html, diff_rec_bf_img, diff_rec_af_html, diff_rec_af_img, high_img_path_of_bf_html, high_img_path_of_af_html)
    # 枠づけ処理をした変更前後のWebページ画像をapp/disp/static/images/sub_effect_pngに保存
    dest_dir = os.path.join(images_dir, "sub_effect_png")
    copy_and_rename_image(subEffect_bf, dest_dir, "bf_sub_effect.png")
    copy_and_rename_image(subEffect_af, dest_dir, "af_sub_effect.png")


    """ 様々な差分画像を差分Webページに表示する """



    """ 以前実行時のcurrent_dirを新しいデータディレクトリの内容に変更 """
    # currentディレクトリがすでに存在する場合は削除
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)
    # 新しいデータディレクトリの内容をcurrentディレクトリにコピー
    shutil.copytree(new_data_dir, current_dir)
    command = f"sudo chown -R aridome:aridome {current_dir}"
    # コマンドを実行
    subprocess.call(command, shell=True)
