todos = []
next_id = 1

def create_todo(title):
    global next_id
    todo = {"id": next_id, "title": title}
    todos.append(todo)
    next_id += 1
    return todo

def update_todo(id, title):
    for todo in todos:
        if todo["id"] == id:
            todo["title"] = title
            return todo
    return None

def delete_todo(id):
    for i, todo in enumerate(todos):
        if todo["id"] == id:
            del todos[i]
            return todo
    return None