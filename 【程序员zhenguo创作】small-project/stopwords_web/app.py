# coding:utf-8

import os
from stopwords import do_stopwords
from util import chi2eng
from flask import Flask, render_template, send_file, make_response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    stop_words = do_stopwords()
    return render_template('index.html', stop_words=stop_words)


@app.route('/stopwords/download/<lang>', methods=['POST'])
def download(lang):
    for lang_i in os.listdir('stopwords'):
        if lang_i == chi2eng[lang]:
            path = os.path.join('stopwords', lang_i)
            response = make_response(send_file(path))
            response.headers["Content-Disposition"] = f"attachment; filename={lang_i}.txt"
            return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
