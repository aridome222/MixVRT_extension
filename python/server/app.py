from flask import Flask, Blueprint, Response, request, send_file, jsonify, render_template, redirect, url_for
import json

from threading import Thread
import subprocess
import os

import sys
sys.path.append('/app/src/module')

# print(sys.path)

import difflib

# from flask_cors import CORS, cross_origin

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
# CORS(MixVRT)
# CORS(app, origins=["http://127.0.0.1:5000"], methods=["GET", "POST"])


""" MixVRTによって枠付き処理をした変更前と後のWebページを表示する用のルーティング """
# 別のカスタムテンプレートフォルダを設定
template_folder2 = os.path.join(diff_dir, 'modified_html', 'templates')
# 新しいBlueprintを作成
new_blueprint = Blueprint('new_blueprint', __name__, template_folder=template_folder2)

# @new_blueprint.route('/modified_testPage_bf')
# def modified_testPage_bf():
#     return render_template('modified_testPage_bf.html')

# @new_blueprint.route('/modified_testPage_af')
# def modified_testPage_af():
#     return render_template('modified_testPage_af.html')

# Blueprintをアプリケーションに登録
MixVRT.register_blueprint(new_blueprint)


""" MixVRTの機能が正しく機能するかを確認する用のルーティング """
# 別のカスタムテンプレートフォルダを設定
template_folder3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'templates')
# 新しいBlueprintを作成
repo = Blueprint('repo', __name__, template_folder=template_folder3)

def clone_or_pull_repo(repo_url, clone_dir):
    clone_thread = None  # 初期化
    if not os.path.exists(clone_dir):
        # Cloneの場合の処理
        clone_thread = Thread(target=subprocess.run, args=(["git", "clone", repo_url, clone_dir],), kwargs={"text": True})  # bufsizeを指定する
        clone_thread.start()
        clone_thread.join()  # Cloneが終了するのを待つ
        print("cloneしました")
        return os.path.join(clone_dir, "templates/index.html")
    else:
        os.chdir(clone_dir)
        # Pullの場合の処理
        pull_thread = Thread(target=subprocess.run, args=(["git", "pull"],), kwargs={"text": True})
        pull_thread.start()
        pull_thread.join()  # Cloneが終了するのを待つ
        print("pullしました")
        # pullの場合のHTMLファイルおよびCSS、JSファイルに変更があるか確認
        html_file_path = os.path.join(clone_dir, "templates/index.html")
        # css_file_path = os.path.join(clone_dir, "static/css/styles.css")
        # js_file_path = os.path.join(clone_dir, "static/js/script.js")
        
        html_last_modified_time = get_file_timestamp(html_file_path)
        # css_last_modified_time = get_file_timestamp(css_file_path)
        # js_last_modified_time = get_file_timestamp(js_file_path)
        
        if has_file_changed(html_file_path, html_last_modified_time):
            print("変更があったため、ファイルを取得します。")
            # 変更がある場合の処理をここに追加
            return html_file_path
        else:
            print("変更がありません。")
            return os.path.join(clone_dir, "templates/index.html")
        # if has_file_changed(html_file_path, html_last_modified_time) or \
        #    has_file_changed(css_file_path, css_last_modified_time) or \
        #    has_file_changed(js_file_path, js_last_modified_time):
        #     print("変更があったため、ファイルを取得します。")
        #     # 変更がある場合の処理をここに追加
        #     return html_file_path
        # else:
        #     print("変更がありません。")
        #     return os.path.join(clone_dir, "templates/index.html")

# 差分情報を取得する関数
def get_diff(old_content, new_content):
    differ = difflib.Differ()
    diff = list(differ.compare(old_content.splitlines(), new_content.splitlines()))
    return '\n'.join(diff)

def has_file_changed(file_path, last_modified_time):
    current_time = os.path.getmtime(file_path)
    return current_time > last_modified_time

def get_file_timestamp(file_path):
    return os.path.getmtime(file_path)

def get_html_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                return os.path.join(root, file)
    return None

@repo.route('/')
def input_url():
    repo_url = "https://github.com/aridome222/web_diff.git"

    # スクリプトが実行されているディレクトリのパス
    current_directory = os.path.dirname(os.path.abspath(__file__))
    clone_dir = os.path.join(current_directory, "cloned_repo")

    # クローンまたはプル後にファイルのタイムスタンプを取得
    html_file = clone_or_pull_repo(repo_url, clone_dir)

    if html_file is not None:
        return render_template("input-url.html")
    else:
        return "HTML-file is Already up to date."

@repo.route('/index', methods=['POST', 'GET'])
# @cross_origin()
def index():
    if request.method == 'POST':
        # POSTリクエストの処理
        page_url = request.form.get('pageUrl')

        # index.htmlにリダイレクト
        return redirect(url_for('render_index', page_url=page_url))
        
    else:
        repo_url = "https://github.com/aridome222/web_diff.git"

        # スクリプトが実行されているディレクトリのパス
        current_directory = os.path.dirname(os.path.abspath(__file__))
        clone_dir = os.path.join(current_directory, "cloned_repo")

        # クローンまたはプル後にファイルのタイムスタンプを取得
        html_file = clone_or_pull_repo(repo_url, clone_dir)

        if html_file is not None:
            # URLを渡してindex.htmlをレンダリング
            return render_template("index.html")
        else:
            return "HTML-file is Already up to date."
        
@repo.route('/before', methods=['POST', 'GET'])
# @cross_origin()
def before_web():
    return render_template("before.html")

@repo.route('/after', methods=['POST', 'GET'])
# @cross_origin()
def after_web():
    return render_template("after.html")

@repo.route('/before_modified', methods=['POST', 'GET'])
# @cross_origin()
def before_modified_web():
    return render_template("before_modified.html")

@repo.route('/after_modified', methods=['POST', 'GET'])
# @cross_origin()
def after_modified_web():
    return render_template("after_modified.html")


@repo.route('/testPage', methods=['POST', 'GET'])
# @cross_origin()
def testPage():
    return render_template("testPage.html")

@repo.route('/testPage_bf', methods=['POST', 'GET'])
# @cross_origin()
def testPage_bf():
    return render_template("testPage_bf.html")

@repo.route('/testPage_af', methods=['POST', 'GET'])
# @cross_origin()
def testPage_af():
    return render_template("testPage_af.html")

@repo.route('/testPage_bf_modified', methods=['POST', 'GET'])
# @cross_origin()
def testPage_bf_modified():
    return render_template("testPage_bf_modified.html")

@repo.route('/testPage_af_modified', methods=['POST', 'GET'])
# @cross_origin()
def testPage_af_modified():
    return render_template("testPage_af_modified.html")


@repo.route('/test1_bf', methods=['POST', 'GET'])
# @cross_origin()
def test1_bf():
    return render_template("test1_bf.html")

@repo.route('/test1_af', methods=['POST', 'GET'])
# @cross_origin()
def test1_af():
    return render_template("test1_af.html")


################################################

# 実験に用いるWebページ

################################################

@repo.route('/experiment/ex1_bf', methods=['POST', 'GET'])
# @cross_origin()
def ex1_bf():
    return render_template("experiment/ex1_bf.html")

@repo.route('/experiment/ex1_af', methods=['POST', 'GET'])
# @cross_origin()
def ex1_af():
    return render_template("experiment/ex1_af.html")





################################################

# 実験に用いるWebページ

################################################


@repo.route('/render_index/<path:page_url>')
# @cross_origin()
def render_index(page_url):
    return render_template("index.html", page_url=page_url)


@repo.route('/piza-form')
def piza_form():
    repo_url = "https://github.com/aridome222/web_diff.git"

    # スクリプトが実行されているディレクトリのパス
    current_directory = os.path.dirname(os.path.abspath(__file__))
    clone_dir = os.path.join(current_directory, "cloned_repo")

    # クローンまたはプル後にファイルのタイムスタンプを取得
    html_file = clone_or_pull_repo(repo_url, clone_dir)

    if html_file is not None:
        return render_template("piza-form.html")
    else:
        return "HTML-file is Already up to date."
    

@repo.route('/log', methods=['POST'])
# @cross_origin()
def log_event():
    data = request.get_json()
    logging.info(f"Log data: {data}")  # ログデータをファイルに書き込む

    return jsonify({"status": "success"}), 200


@repo.route('/console', methods=['POST'])
def log():
    log_data = request.json
    print(log_data)  # コンソールに出力
    # 必要に応じてファイルやデータベースにログを保存
    # 例: ファイルに保存
    with open('log.txt', 'a') as f:
        json.dump(log_data, f)
        f.write('\n')

    return jsonify({'status': 'success'})


# @repo.route('/diff', methods=['POST'])
# # @cross_origin()
# def diff():
#     data = request.get_json()
#     url1 = data.get('url1')
#     url2 = data.get('url2')

#     # 差分検出プログラムを実行して差分画像のパスを取得
#     diff_img1, diff_img2 = run_diff_program(url1, url2)

#     return jsonify({'diff_image_url1': diff_img1, 'diff_image_url2': diff_img2})


@repo.route('/confirmation', methods=['POST'])
def confirmation():
    # フォームからデータを取得
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    pizza_type = request.form.get('pizza-type')
    pizza_size = request.form.get('pizza-size')
    pizza_quantity = request.form.get('pizza-quantity')
    delivery_time = request.form.get('delivery-time')
    comments = request.form.get('comments')

    # テンプレートにデータを渡して確認ページをレンダリング
    return render_template('confirmation.html', name=name, phone=phone, email=email, pizza_type=pizza_type, pizza_size=pizza_size, pizza_quantity=pizza_quantity, delivery_time=delivery_time, comments=comments)

# Blueprintをアプリケーションに登録
MixVRT.register_blueprint(repo)



@MixVRT.route('/MixVRT_url', methods=['POST', 'GET'])
# @cross_origin()
def MixVRT_url():
    return render_template('MixVRT_url.html')

@MixVRT.route('/MixVRT_diff', methods=['POST', 'GET'])
# @cross_origin()
def MixVRT_diff():
    return render_template('MixVRT_diff.html')

@MixVRT.route('/MixVRT_test', methods=['POST', 'GET'])
# @cross_origin()
def MixVRT_test():
    return render_template('MixVRT_test.html')

@MixVRT.route('/MixVRT_test_af', methods=['POST', 'GET'])
# @cross_origin()
def MixVRT_test_af():
    return render_template('MixVRT_test_af.html')

@MixVRT.route('/before', methods=['POST', 'GET'])
# @cross_origin()
def before():
    return render_template('before.html')

@MixVRT.route('/after', methods=['POST', 'GET'])
# @cross_origin()
def after():
    return render_template('after.html')

@MixVRT.route('/ari_eval_bf', methods=['POST', 'GET'])
# @cross_origin()
def ari_eval_bf():
    return render_template('ari_eval_bf.html')

@MixVRT.route('/ari_eval_af', methods=['POST', 'GET'])
# @cross_origin()
def ari_eval_af():
    return render_template('ari_eval_af.html')

@MixVRT.route('/ari_eval', methods=['POST', 'GET'])
# @cross_origin()
def ari_eval():
    return render_template('ari_eval.html')

@MixVRT.route('/test', methods=['POST', 'GET'])
# @cross_origin()
def test():
    return render_template('test.html')

@MixVRT.route('/modified_testPage_bf')
def modified_testPage_bf():
    return render_template('modified_testPage_bf.html')

@MixVRT.route('/modified_testPage_af')
def modified_testPage_af():
    return render_template('modified_testPage_af.html')

if __name__ == '__main__':
    MixVRT.run(host='0.0.0.0', port=5000, debug=True)
