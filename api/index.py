from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 30px 15px;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 40px rgba(0,0,0,.2);
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #222;
        }

        .input-box {
            display: flex;
            gap: 10px;
        }

        #todoInput {
            flex: 1;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 10px;
            outline: none;
            font-size: 16px;
        }

        button {
            border: none;
            cursor: pointer;
            border-radius: 10px;
            padding: 12px 16px;
            font-weight: bold;
        }

        .add-btn {
            background: #667eea;
            color: white;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            font-size: 14px;
            color: #666;
        }

        .filters {
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
        }

        .filters button {
            background: #f1f1f1;
        }

        .filters button.active {
            background: #667eea;
            color: white;
        }

        ul {
            list-style: none;
        }

        li {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 13px;
            margin-bottom: 10px;
            background: #f7f7f7;
            border-radius: 10px;
        }

        li span {
            flex: 1;
            word-break: break-word;
        }

        li.completed span {
            text-decoration: line-through;
            color: #999;
        }

        .edit {
            background: #ffc107;
            color: #222;
        }

        .delete {
            background: #ff4d4d;
            color: white;
        }

        .empty {
            text-align: center;
            color: #999;
            padding: 25px;
        }

        @media (max-width: 500px) {
            .input-box {
                flex-direction: column;
            }

            .add-btn {
                width: 100%;
            }

            li {
                flex-wrap: wrap;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <h1>📝 My Todo List</h1>

    <div class="input-box">
        <input id="todoInput" type="text" placeholder="Enter your task...">
        <button class="add-btn" onclick="addTodo()">Add</button>
    </div>

    <div class="stats">
        <span>Total: <b id="total">0</b></span>
        <span>Completed: <b id="completed">0</b></span>
        <span>Pending: <b id="pending">0</b></span>
    </div>

    <div class="filters">
        <button class="active" onclick="setFilter('all', this)">All</button>
        <button onclick="setFilter('pending', this)">Pending</button>
        <button onclick="setFilter('completed', this)">Completed</button>
    </div>

    <ul id="todoList"></ul>

</div>

<script>
    let todos = JSON.parse(localStorage.getItem("todos")) || [];
    let filter = "all";

    function save() {
        localStorage.setItem("todos", JSON.stringify(todos));
    }

    function addTodo() {
        const input = document.getElementById("todoInput");
        const text = input.value.trim();

        if (!text) {
            alert("Please enter a task!");
            return;
        }

        todos.push({
            id: Date.now(),
            text: text,
            completed: false
        });

        input.value = "";
        save();
        render();
    }

    function toggleTodo(id) {
        todos = todos.map(todo =>
            todo.id === id
                ? {...todo, completed: !todo.completed}
                : todo
        );

        save();
        render();
    }

    function deleteTodo(id) {
        todos = todos.filter(todo => todo.id !== id);
        save();
        render();
    }

    function editTodo(id) {
        const todo = todos.find(t => t.id === id);
        const newText = prompt("Edit task:", todo.text);

        if (newText !== null && newText.trim() !== "") {
            todo.text = newText.trim();
            save();
            render();
        }
    }

    function setFilter(value, button) {
        filter = value;

        document.querySelectorAll(".filters button")
            .forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

        render();
    }

    function render() {
        const list = document.getElementById("todoList");

        let filtered = todos;

        if (filter === "pending") {
            filtered = todos.filter(todo => !todo.completed);
        }

        if (filter === "completed") {
            filtered = todos.filter(todo => todo.completed);
        }

        list.innerHTML = "";

        if (filtered.length === 0) {
            list.innerHTML = '<div class="empty">No tasks found 🎉</div>';
        }

        filtered.forEach(todo => {
            const li = document.createElement("li");

            if (todo.completed) {
                li.classList.add("completed");
            }

            li.innerHTML = `
                <input
                    type="checkbox"
                    ${todo.completed ? "checked" : ""}
                    onchange="toggleTodo(${todo.id})"
                >

                <span>${escapeHTML(todo.text)}</span>

                <button class="edit"
                    onclick="editTodo(${todo.id})">
                    Edit
                </button>

                <button class="delete"
                    onclick="deleteTodo(${todo.id})">
                    Delete
                </button>
            `;

            list.appendChild(li);
        });

        const completed = todos.filter(t => t.completed).length;

        document.getElementById("total").textContent = todos.length;
        document.getElementById("completed").textContent = completed;
        document.getElementById("pending").textContent =
            todos.length - completed;
    }

    function escapeHTML(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    document.getElementById("todoInput").addEventListener("keydown", e => {
        if (e.key === "Enter") {
            addTodo();
        }
    });

    render();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run()
