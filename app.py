import os
from flask import (Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://Shashasha21:jk7nMqjBp6jvVDV@myfirstcluster.z9kcu.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add_task")
def add_task():
    return render_template("addtask.html",
    categories=mongo.db.categories.find())

@app.route('/insert_task', methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id" : ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)