from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Set absolute directory for the database.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# Class that calls db.Model and defines id, content, and date_created.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # I do not know what this does yet.
    def __repr__(self):
        return "<Task %r>" % self.id
    

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        if len(task_content) < 1:
            return redirect("/")
        else:
            new_task = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect("/")
            except:
                return "There was an issue adding your task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return f"There was an issue deleting that task (id: {task_to_delete})"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return f"There was an issue updating your task (id: {task_to_update})"

    else:
        return render_template("update.html", task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)