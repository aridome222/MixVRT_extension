from flask import Flask, request, abort
import hmac
import hashlib

import os
import subprocess
import shutil

app = Flask(__name__)

SECRET = "aridome_codeless"  # GitHub Webhookの設定に合わせて設定

@app.route('/webhook', methods=['POST'])
def webhook():
    # リクエストがJSONであることを確認
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Invalid content type')

    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature')

    # シグネチャがない場合はエラー
    if signature is None:
        abort(400, 'X-Hub-Signature header is missing')

    # シグネチャを検証
    if not verify_signature(payload, signature):
        abort(403, 'Invalid signature')

    data = request.json
    if 'push' in data.get('event', ''):
        # プッシュイベントが発生した場合の処理
        handle_push_event(data)

    return '', 200

def verify_signature(payload, signature):
    # Webhookリクエストの署名を検証
    sha_name, signature = signature.split('=')
    if sha_name != 'sha1':
        return False

    # GitHubのWebhookシークレットを使ってHMACを計算
    mac = hmac.new(SECRET.encode('utf-8'), msg=payload, digestmod=hashlib.sha1)

    # 計算された署名と送られてきた署名を比較
    return hmac.compare_digest(mac.hexdigest(), signature)

def handle_push_event(data):
    # スクリプトが実行されているディレクトリのパス
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # クローン先ディレクトリの相対パス
    clone_directory = os.path.join(current_directory, "python", "cloned_repo")

    # リポジトリのURL（例: https://github.com/your-username/your-repo.git）
    repo_url = "https://github.com/aridome222/Zenn_selenium.git"

    try:
        # リポジトリをクローン
        subprocess.run(["git", "clone", repo_url, clone_directory])

        # コピー先ディレクトリが存在しない場合は作成
        destination_path = os.path.join(current_directory, "python", "html")
        os.makedirs(destination_path, exist_ok=True)

        # クローンされたリポジトリ内の特定のディレクトリやファイルをサーバに転送
        source_path = os.path.join(clone_directory, "html", "test.html")

        # ファイルをコピー
        shutil.copy2(source_path, destination_path)

        print(f"Repository cloned and files transferred successfully to: {destination_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    app.run(host='172.24.66.152', port=5000)
