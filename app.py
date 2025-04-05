from flask import Flask, render_template, request, redirect

app = Flask(__name__)
TASKS_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        tasks = load_tasks()
        tasks.append("[ ] " + task)
        save_tasks(tasks)
    return redirect("/")

@app.route("/done/<int:task_id>")
def done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        if tasks[task_id].startswith("[ ]"):
            tasks[task_id] = tasks[task_id].replace("[ ]", "[✓]", 1)
        elif tasks[task_id].startswith("[✓]"):
            tasks[task_id] = tasks[task_id].replace("[✓]", "[ ]", 1)
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
