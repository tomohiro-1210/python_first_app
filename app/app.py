from flask import Flask , render_template,g,redirect,request #render_templateはフォルダの読み込みに必要
import sqlite3
DATABASE="flaskmemo2.db"
from flask_login import UserMixin,LoginManager,login_required,login_user,logout_user
import os
from werkzeug.security import generate_password_hash,check_password_hash

# ログイン機能
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

#ログイン
class User(UserMixin):
    def __init__(self,userid):
        self.id = userid

@login_manager.user_loader
def load_user(userid):
    return User(userid)
# ログイン画面に自動遷移
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

# ログインへのルート
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = ''
    userid = ''

    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        #ログインチェック
        user_data = get_db().execute(
            "select password from user where userid=?", [userid,]
        ).fetchone()

        if user_data is not None:
            if check_password_hash(user_data[0],password):
                user = User(userid)
                login_user(user)
                return redirect('/')
            
            error_message = 'ログインIDとパスワードが間違っています。'

    return render_template('login.html', userid=userid, error_message=error_message)

#ログアウトへのルート
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

#新規登録
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = ""

    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        pw_hash = generate_password_hash(password, method='pbkdf2:sha256')

        #DB登録
        db = get_db()
        user_check = get_db().execute("select userid from user where userid=?", [userid,]).fetchall()
        if not user_check:
            db.execute(
                "insert into user (userid, password) values (?, ?)", 
                (userid, pw_hash)
            )
            db.commit()
            return redirect('/login')
        else:
            error_message = "入力されたユーザーidは既に登録されています。"


    return render_template('signup.html')

# 127・・・/<name>でURLを入力したとき関数で返せるようにする
@app.route("/")
@login_required #ログインしているかの判定
def top():
    memo_list = get_db().execute("select id, title, body from memo").fetchall()
    return render_template('index.html', memo_list=memo_list) 

if __name__ == "__main__":
    app.run()

# 登録画面
@app.route("/regist", methods=['GET', 'POST'])
@login_required #ログインしているかの判定
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
@login_required #ログインしているかの判定
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
@login_required #ログインしているかの判定
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

