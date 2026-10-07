from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>My Todo List</h1>
    <p>Todo App is working!</p>
    """

if __name__ == "__main__":
    app.run()
