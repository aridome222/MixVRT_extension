from flask import Flask, render_template
from threading import Thread
import subprocess
import os


# カスタムテンプレートフォルダと静的フォルダを設定
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

def clone_or_pull_repo(repo_url, clone_dir):
    clone_thread = None  # 初期化
    if not os.path.exists(clone_dir):
        # Cloneの場合の処理
        clone_thread = Thread(target=subprocess.run, args=(["git", "clone", repo_url, clone_dir],), kwargs={"text": True})  # bufsizeを指定する
        clone_thread.start()
        clone_thread.join()  # Cloneが終了するのを待つ
        print("cloneしました")
        # cloneの場合の特定の処理
        print("Cloneの場合の特定の処理を実行します。")
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
