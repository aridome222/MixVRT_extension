from flask import Flask, Blueprint, Response, request, jsonify, render_template, redirect, url_for
import json

from threading import Thread
import subprocess
import os

import sys
sys.path.append('/app/src/module')

# print(sys.path)

import difflib

from flask_cors import CORS, cross_origin

import pytest
import shlex
import logging

# 基本ディレクトリの設定
disp_dir = "app/disp"
# 絶対パス指定
disp_dir =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), disp_dir)

diff_dir = "app/diff_dir"
# 絶対パス指定
diff_dir =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), diff_dir)


""" MixVRTによる視覚的回帰テストの結果を表示する用のWebページ """
# カスタムテンプレートフォルダと静的フォルダを設定
template_folder = os.path.join(disp_dir, 'templates')
static_folder = os.path.join(disp_dir, 'static')
MixVRT = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
CORS(MixVRT)
# CORS(app, origins=["http://127.0.0.1:5000"], methods=["GET", "POST"])


""" MixVRTによって枠付き処理をした変更前と後のWebページを表示する用のルーティング """
# 別のカスタムテンプレートフォルダを設定
template_folder2 = os.path.join(diff_dir, 'modified_html', 'templates')
# 新しいBlueprintを作成
new_blueprint = Blueprint('new_blueprint', __name__, template_folder=template_folder2)

@new_blueprint.route('/modified_testPage_bf')
def modified_testPage_bf():
    return render_template('modified_testPage_bf.html')

@new_blueprint.route('/modified_testPage_af')
def modified_testPage_af():
    return render_template('modified_testPage_af.html')

# Blueprintをアプリケーションに登録
MixVRT.register_blueprint(new_blueprint)


@MixVRT.route('/MixVRT_url', methods=['POST', 'GET'])
@cross_origin()
def MixVRT_url():
    return render_template('MixVRT_url.html')

@MixVRT.route('/MixVRT_diff', methods=['POST', 'GET'])
@cross_origin()
def MixVRT_diff():
    return render_template('MixVRT_diff.html')


if __name__ == '__main__':
    MixVRT.run(host='0.0.0.0', port=5000, debug=True)
