from flask import Flask , render_template,g,redirect,request #render_templateはフォルダの読み込みに必要
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

# 登録画面
@app.route("/regist", methods=['GET', 'POST'])
def regist():
    if request.method == "POST":
        #登録画面からの情報取得
        title = request.form.get('title')
        body = request.form.get('body')
        db = get_db() #DBの情報ゲット
        db.execute("insert into memo (title,body) values(?,?)", [title,body]) #DBに情報を挿入
        db.commit() #実行
        return redirect('/')

    return render_template('regist.html')

# 編集画面
@app.route("/<id>/edit", methods=['GET', 'POST'])
def edit(id):
    if request.method == "POST":
        #登録画面からの情報取得
        title = request.form.get('title')
        body = request.form.get('body')
        db = get_db() #DBの情報ゲット
        db.execute("update memo set title=?, body=? where id=?", [title,body,id]) #DBに情報を挿入
        db.commit() #実行
        return redirect('/')
    #DBに登録
    post = get_db().execute(
        "select id,title,body from memo where id=?", (id,)
    ).fetchone()
    return render_template('edit.html',post=post)

#削除画面
@app.route("/<id>/delete", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        db = get_db() #DBの情報ゲット
        db.execute("delete from memo where id=?", [id,]) #DBに情報を挿入
        db.commit() #実行
        return redirect('/')
    #DBに登録
    
    post = get_db().execute(
        "select id,title,body from memo where id=?" , (id,)
    )
    
    return render_template('delete.html', post=post)

#DBへアクセス
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

