from flask import Flask , render_template #render_templateはフォルダの読み込みに必要

app = Flask(__name__)

# リスト、ここは分けたほうがよさそうだなという印象。
list = [
    'test0',
    'test1',
    'test2',
    'test3',
    'test4',
    'test5',
    'test6',
    'test7',
]

# 127・・・/<name>でURLを入力したとき関数で返せるようにする
@app.route("/<name>")
def H(name):
    return render_template('index.html', name=name, list=list) # Wクォートではなくシングルクォートで囲む

# topページを表示させる場合
# @app.route("/")
# def H_top():
#     return render_template('index.html') # Wクォートではなくシングルクォートで囲む

if __name__ == "__main__":
    app.run()