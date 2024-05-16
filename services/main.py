from api.auth import Register, Login
from api.projects import ProjectGroup, ProjectItem
from api.tasks import TasksGroup, TaskItem
from app import app


def main():
    app.add_url_rule(rule="/register", view_func=Register.as_view("register-hehe"), methods=["POST"])
    app.add_url_rule(rule="/login", view_func=Login.as_view("login-hehe"), methods=["POST"])
    app.add_url_rule(rule="/projects/<id>/tasks/<item_id>",
                     view_func=TaskItem.as_view("project-id-tasks-itemid"), methods=["PUT", "GET", "DELETE"])
    app.add_url_rule(rule="/projects/<id>/tasks", view_func=TasksGroup.as_view("tasks"),
                     methods=["GET", "POST"])
    app.add_url_rule(rule="/projects/<id>", view_func=ProjectItem.as_view("projects-id"),
                     methods=["GET", "PUT", "DELETE"])
    app.add_url_rule(rule="/projects", view_func=ProjectGroup.as_view("projects"), methods=["GET", "POST"])
    app.run(debug=True)


if __name__ == "__main__":
    main()
