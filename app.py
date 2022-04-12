from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route("/")
def home():
    final = Todo.query.all()
    return render_template("index.html", final=final)


@app.route("/do", methods=["POST"])
def add():
    txt = request.form.get("todo")
    to_do = Todo(job=txt, done=False)
    db.session.add(to_do)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/status/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/del/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
