from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 处理添加任务
        task_content = request.form["task"]
        if task_content == '':
            return redirect("/")
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "加载首页有问题"
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "删除时候有问题"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["task"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "更新有问题"
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()

        return render_template("index.html", task_updated=task, tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
