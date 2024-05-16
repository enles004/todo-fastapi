import os

from dotenv import load_dotenv

load_dotenv()

psql_url = os.getenv("PSQL_URL")
result_backend = os.getenv("RESULT_BACKEND")


class Config(object):
    CACHE_TYPE = os.environ["CACHE_TYPE"]
    CACHE_REDIS_HOST = os.environ["CACHE_REDIS_HOST"]
    CACHE_REDIS_PORT = os.environ["CACHE_REDIS_PORT"]
    CACHE_REDIS_DB = os.environ["CACHE_REDIS_DB"]
    CACHE_DEFAULT_TIMEOUT = os.environ["CACHE_DEFAULT_TIMEOUT"]


secret_key = os.getenv("SECRET_KEY")
sender_email = os.getenv("SENDER_EMAIL")
pass_email = os.getenv("PASS_EMAIL")
local = os.getenv("LOCAL")
queue_user_account = os.getenv("QUEUE_USER_ACCOUNT")
queue_delete_project = os.getenv("QUEUE_DELETE_PROJECT")
smtp_server = os.getenv("SMTP_SEVER")
smtp_port = os.getenv("SMTP_PORT")

rabbitmq_config_user = {"host": local, "queue": queue_user_account}
rabbitmq_config_project = {"host": local, "queue": queue_delete_project}
broker_url = os.getenv("BROKER_URL")
mongo_url = os.getenv("MONGO_URL")
