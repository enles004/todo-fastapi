from functools import wraps

from db.session import permissions
from db.session import role_per, users


def check_permissions(required_permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs["user"]["user_id"]
            if not user_id:
                return {"Message": "The user not logged in"}
            role_user = users.find_one({"_id": user_id})
            user_permission = role_per.find({"role_name": role_user["role"]})
            permission = []
            for user_per in list(user_permission):
                permission.append(permissions.find_one({"name": user_per["per_name"]})["name"])

            if not any(per in permission for per in required_permission):
                return {"Message": "User does not have permissions"}
            return await func(*args, **kwargs)

        return wrapper

    return decorator
