# Users
users = {"_id": "",
         "email": "",
         "username": "",
         "password": "",
         "role": "",
         "created": ""}

# Projects
projects = {"_id": "",
            "user_id": "",
            "name": "",
            "action": "",
            "created": ""}

# Tasks
tasks = {"_id": "",
         "project_id": "",
         "title": "",
         "name": "",
         "expiry": "",
         "action": "",
         "date_completed": "",
         "created": ""}

# Authorization
roles = {"_id": "",
         "name": ""}

permissions = {"_id": "",
               "name": ""}

role_per = {"_id": "",
            "role": roles["name"],
            "per": permissions["name"]}