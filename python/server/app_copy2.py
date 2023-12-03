from flask import Flask, render_template
from threading import Thread
import os
import time

from difflib import unified_diff
from git import Repo

# カスタムテンプレートフォルダと静的フォルダを設定
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloned_repo', 'static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

def clone_or_pull_repo(repo_url, clone_dir):
    repo = None
    html_file_path = os.path.join(clone_dir, "templates/index.html")
    css_file_path = os.path.join(clone_dir, "static/css/styles.css")
    js_file_path = os.path.join(clone_dir, "static/js/script.js")

    if not os.path.exists(clone_dir):
        # Cloneの場合の処理
        Repo.clone_from(repo_url, clone_dir)
        print("cloneしました")
        repo = Repo(clone_dir)
        return os.path.join(clone_dir, "templates/index.html")
    else:
        os.chdir(clone_dir)
        old_content = read_file(html_file_path)
        # Pullの場合の処理
        repo = Repo(clone_dir)
        origin = repo.remote('origin')
        origin.pull()
        print("pullしました")

        # タイムスタンプのデバッグログ
        current_time = int(time.mktime(time.localtime()))
        html_last_modified_time = int(get_file_timestamp(html_file_path))
        css_last_modified_time = int(get_file_timestamp(css_file_path))
        js_last_modified_time = int(get_file_timestamp(js_file_path))

        print(f"Current Time: {current_time}")
        print(f"HTML Last Modified Time: {html_last_modified_time}")
        print(f"CSS Last Modified Time: {css_last_modified_time}")
        print(f"JS Last Modified Time: {js_last_modified_time}")

        if has_file_changed(html_file_path, html_last_modified_time) or \
           has_file_changed(css_file_path, css_last_modified_time) or \
           has_file_changed(js_file_path, js_last_modified_time):
            print("変更があったため、ファイルを取得します。")
            # 変更がある場合の処理をここに追加
            new_content = read_file(html_file_path)
            print("Old Content:")
            print(old_content)
            
            print("New Content:")
            print(new_content)
            save_diff_info(old_content, new_content)
            
            return html_file_path
        else:
            print("変更がありません。")
            return os.path.join(clone_dir, "templates/index.html")

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_diff_info(old_content, new_content):
    diff_info = list(unified_diff(old_content.splitlines(), new_content.splitlines()))
    with open('diff_info.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(diff_info))

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
    app.run(host='0.0.0.0', port=5000, debug=False)
