print("これがgithubに行ったら無事にpushされている証拠")

sanin_trains = ["やくも", "スーパーいなば" ,"スーパーまつかぜ", "スーパーおき" , "スーパーはくと", "はまかぜ"]
print(sanin_trains)

django = "Djangoは大規模なアプリ開発に向いているFW。"
flask = "Flaskは小規模アプリ開発にむいているFW"

#仮想環境とFlaskバージョンはセット。
#別のFlaskバージョンで開発する場合はまた仮想環境構築が必要になってくる。
#仮想環境構築方法> https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/installation.html

#※powerShellで仮想環境構築が管理者権限で実行できないときは下記コード
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 管理者権限を元に戻すときは下記コードでセキュリティーを戻す
# Set-ExecutionPolicy Restricted -Scope CurrentUser

#flaskを動かすコマンド
# venv\Scripts\Activate

# flaskを実行するコマンド（PowerShell）
# １．$env:FLASK_APP = "app.py"
# 2.flask run

# (ディレクトリ)/templatesフォルダの中にhtmlフォルダを置く（CSSもあり？）
# render_templateでフォルダを読み込む

#flask_loginインストール
#pip install falsk-login