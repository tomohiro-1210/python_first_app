from flask import Flask , render_template,g #render_templateはフォルダの読み込みに必要
import sqlite3
DATABASE="flaskmemo2.db"

app = Flask(__name__)


# 127・・・/<name>でURLを入力したとき関数で返せるようにする
@app.route("/")
def top():
    memo_list = get_db().execute("select id, title, body from memo").fetchall()
    return render_template('index.html', memo_list=memo_list) 

if __name__ == "__main__":
    app.run()

    
#DBへアクセス
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

