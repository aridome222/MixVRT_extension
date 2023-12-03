from flask import Flask

import subprocess
import os

app = Flask(__name__)

def clone_or_pull_repo(repo_url, clone_dir):
    if not os.path.exists(clone_dir):
        subprocess.run(["git", "clone", repo_url, clone_dir])
    else:
        os.chdir(clone_dir)
        subprocess.run(["git", "pull"])

@app.route('/')
def hello():
    repo_url = "git@github.com:aridome222/web_diff.git"

    # スクリプトが実行されているディレクトリのパス
    current_directory = os.path.dirname(os.path.abspath(__file__))
    clone_dir = os.path.join(current_directory, "cloned_repo")
    
    clone_or_pull_repo(repo_url, clone_dir)
    
    return "Clone or pull Successful!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
