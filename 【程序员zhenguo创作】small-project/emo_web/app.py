# coding:utf-8
import myemo
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = '214S%yjX#l'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    target = request.form['target']
    emo_list = myemo.search(target)
    if not emo_list:
        flash("未找到")
    return render_template('index.html', emo_list=emo_list, target=target)


@app.route('/search_all', methods=['GET'])
def search_all():
    emo_list = myemo.search_all()
    if not emo_list:
        flash("未找到")
    return render_template('index.html', emo_list=emo_list)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
