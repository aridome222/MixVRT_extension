from flask import Flask, request, jsonify, render_template
from threading import Thread
import subprocess
import os

import sys
sys.path.append('/app/src/module')
# print(sys.path)

import difflib

from flask_cors import CORS, cross_origin

from main import main
from src.module import detect_rec_divide
from src.module import test_slt_addShot
import pytest
import shlex


# カスタムテンプレートフォルダと静的フォルダを設定
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
CORS(app)


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
        css_file_path = os.path.join(clone_dir, "static/css/styles.css")
        js_file_path = os.path.join(clone_dir, "static/js/script.js")
        
        html_last_modified_time = get_file_timestamp(html_file_path)
        css_last_modified_time = get_file_timestamp(css_file_path)
        js_last_modified_time = get_file_timestamp(js_file_path)
        
        if has_file_changed(html_file_path, html_last_modified_time) or \
           has_file_changed(css_file_path, css_last_modified_time) or \
           has_file_changed(js_file_path, js_last_modified_time):
            print("変更があったため、ファイルを取得します。")
            # 変更がある場合の処理をここに追加
            return html_file_path
        else:
            print("変更がありません。")
            return os.path.join(clone_dir, "templates/index.html")

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

@app.route('/index')
def index():
    repo_url = "https://github.com/aridome222/web_diff.git"

    # スクリプトが実行されているディレクトリのパス
    current_directory = os.path.dirname(os.path.abspath(__file__))
    clone_dir = os.path.join(current_directory, "cloned_repo")

    # クローンまたはプル後にファイルのタイムスタンプを取得
    html_file = clone_or_pull_repo(repo_url, clone_dir)

    if html_file is not None:
        return render_template("index.html")
    else:
        return "HTML-file is Already up to date."


@app.route('/diff', methods=['POST'])
@cross_origin()
def diff():
    data = request.get_json()
    url1 = data.get('url1')
    url2 = data.get('url2')

    # 差分検出プログラムを実行して差分画像のパスを取得
    diff_img1, diff_img2 = run_diff_program(url1, url2)

    return jsonify({'diff_image_url1': diff_img1, 'diff_image_url2': diff_img2})


@app.route('/confirmation', methods=['POST'])
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


def run_diff_program(url1, url2):
    # URLのエスケープ確認
    print(f"url1: {url1}")
    print(f"url2: {url2}")

    # まず、テストを呼び出すためにsys.argvを準備
    sys.argv = [
        "pytest",
        "-s",
        "-v",
        "--cache-clear",
        "/python/src/module/test_slt_addShot.py",
        "-k",
        "test_singlelinetext",
        "--",
        url1,  # ここでテストメソッドに渡す引数を指定
    ]

    # テストの実行
    with pytest.warns(None) as record:  # Noneを渡すことで全ての警告を無視
        pytest.main()

    # デバッグのためにrecordを出力
    print("-------------------------")
    print(record)
    print("-------------------------")

    # recordが空の場合に対処
    if record:
        # ここで差分検出プログラムを実行
        # 例: subprocess.run(['python', 'path/to/your_diff_program.py', img1_path, img2_path], check=True)
        # 実際のプログラムのパスと引数は適切に設定してください

        # 引数を適切にエスケープ
        url1_escaped = shlex.quote(url1)

        # コマンドの実行
        cmd1 = f"docker exec -it zenn_selenium-python-1 python -m pytest -s --cache-clear /python/src/test_slt_addShot.py {url1_escaped}"
        print(f"cmd1: {cmd1}")
        result1 = subprocess.run(cmd1, text=True, shell=True)
        print(f"stdout1: {result1.stdout}")
        print(f"stderr1: {result1.stderr}")
        img1_path = result1.stdout.strip()

        # 同じことをurl2に対して繰り返します
        sys.argv[-1] = url2

        # 引数を適切にエスケープ
        url2_escaped = shlex.quote(url2)

        # コマンドの実行
        cmd2 = f"docker exec -it zenn_selenium-python-1 python -m pytest -s --cache-clear /python/src/test_slt_addShot.py {url2_escaped}"
        print(f"cmd2: {cmd2}")
        result2 = subprocess.run(cmd2, text=True, shell=True)
        print(f"stdout2: {result2.stdout}")
        print(f"stderr2: {result2.stderr}")
        img2_path = result2.stdout.strip()

        # デバッグのためにrecordを出力
        print("-------------------------")
        print(record)
        print("-------------------------")

        diff_img1, diff_img2 = detect_rec_divide.main(img1_path, img2_path)
        return diff_img1, diff_img2
    else:
        # recordが空の場合、エラー処理またはデフォルトの値を返すなど、適切な対処を行う
        return None, None


# def run_diff_program(url1, url2):
#     # ここで差分検出プログラムを実行
#     # 例: subprocess.run(['python', 'path/to/your_diff_program.py', url1, url2], check=True)
#     # 実際のプログラムのパスと引数は適切に設定してください
#     # 生成された差分画像のパスを返す

#     # test_slt_addShot.py を直接呼び出して、生成された差分画像のファイルパスを取得
#     cmd1 = "docker exec -it zenn_selenium-python-1 python -m pytest -s --cache-clear /python/src/test_slt_addShot.py " + url1
#     result1 = subprocess.run(cmd1, text=True, capture_output=True, shell=True)
#     img1_path = result1.stdout.strip()

#     cmd2 = "docker exec -it zenn_selenium-python-1 python -m pytest -s --cache-clear /python/src/test_slt_addShot.py " + url2
#     result2 = subprocess.run(cmd2, text=True, capture_output=True, shell=True)
#     img2_path = result2.stdout.strip()

#     diff_img1, diff_img2 = detect_rec_divide.main(img1_path, img2_path)
    
#     return diff_img1, diff_img2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
