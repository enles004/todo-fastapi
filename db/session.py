from redis import Redis
from pymongo import MongoClient
# from redis import Redis
import config
client = MongoClient(config.mongo_url)
db = client.todolist

users = db.users
projects = db.projects
tasks = db.tasks
roles = db.roles
permissions = db.permissions
role_per = db.role_per

r = Redis(host="localhost", port=6379, decode_responses=True)