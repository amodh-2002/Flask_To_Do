from flask import Flask, render_template, request, redirect, url_for
from ariadne import QueryType, MutationType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML 
from utils import todos, create_todo, update_todo, delete_todo

type_defs = open("schema.graphql").read()

query = QueryType()
mutation = MutationType()

@query.field("todos")
def resolve_todos(*_):
    return todos

@mutation.field("createTodo")
def resolve_create_todo(_, info, title):
    todo = create_todo(title)
    return todo

@mutation.field("updateTodo")
def resolve_update_todo(_, info, id, title):
    todo = update_todo(id, title)
    return todo

@mutation.field("deleteTodo")
def resolve_delete_todo(_, info, id):
    todo = delete_todo(id)
    return todo

schema = make_executable_schema(type_defs, [query, mutation])

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", todos=todos)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        create_todo(title)
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    todo = next((t for t in todos if t["id"] == id), None)
    if request.method == "POST":
        title = request.form["title"]
        update_todo(id, title)
        return redirect(url_for("index"))
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    todo = next((t for t in todos if t["id"] == id), None)
    if request.method == "POST":
        delete_todo(id)
        return redirect(url_for("index"))
    return render_template("delete.html", todo=todo)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 200 if success else 400
    return result, status_code

if __name__ == '__main__':
    app.run(debug=True)