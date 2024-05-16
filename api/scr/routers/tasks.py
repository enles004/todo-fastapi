from datetime import datetime
from typing import Annotated

from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, Body

from api.middleware.authentication import current_user
from api.middleware.authorization import check_permissions
from api.schema.schema_task import TaskPayload, TaskParams
from db.session import projects, tasks
from handlers.params import filtering

router = APIRouter()


# TASK_GROUP
@router.post("/project/{id}/task")
@check_permissions(["write"])
async def create_task(id,
                      user: Annotated[dict, Depends(current_user)],
                      payload: Annotated[TaskPayload, Body(embed=True)
                      ]):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "no project"}
    try:
        date = datetime.strptime(payload.expiry, "%Y-%m-%d %H:%M:%S")
    except (KeyError, ValueError):
        now = datetime.now()
        date = datetime(now.year, now.month, now.day + 1)
    new_task = {"_id": str(ObjectId()),
                "project_id": id,
                "title": payload.title,
                "name": payload.name,
                "expiry": date,
                "action": False,
                "date_complete": None,
                "created": datetime.now()}
    try:
        tasks.insert_one(new_task)
    except Exception:
        return {"message": "error"}
    data = {"id": new_task["_id"],
            "title": new_task["title"],
            "name": new_task["name"],
            "expiry": new_task["expiry"],
            "action": new_task["action"]}
    return data, 201


@router.get("/project/{id}/task")
@check_permissions(["read"])
async def get_task(id,
                   user: Annotated[dict, Depends(current_user)],
                   query_params: Annotated[TaskParams, Depends()]
                   ):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "no project"}, 404
    if query_params:
        # Pagination
        page = query_params.page
        per_page = query_params.per_page
        offset = (page - 1) * per_page

        # Filtering
        fil = {"project_id": project["_id"]}
        data_fil = {"title": query_params.title,
                    "name": query_params.name,
                    "id": query_params.id_task,
                    "action": query_params.action}

        for key, value in data_fil.items():
            if value:
                if key == "name" or key == "title":
                    fil.update(filtering({key: value}))
                else:
                    fil.update({key: value})

        # Sorting
        query = tasks
        if query_params.order == "asc":
            query = tasks.find(fil).sort(query_params.sort_by, 1).skip(offset).limit(per_page)
        elif query_params.order == "desc":
            query = tasks.find(fil).sort(query_params.sort_by, -1).skip(offset).limit(per_page)

        # Result
        result = list(query)
        total = len(result)
        return {"data": [
            {"title": data["title"], "name": data["name"], "created": data["created"], "id": str(data["_id"]),
             "date_completed": data["date_complete"], "action": data["action"]} for data in result],
            "meta": [{"page": page, "per_page": per_page, "total": total}]}, 200


# TASK_ITEM
@router.get("/project/{id}/task/{item_id}")
@check_permissions(["read"])
async def get_task_by_id(id,
                         user: Annotated[dict, Depends(current_user)],
                         item_id):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "no project"}, 404
    task = tasks.find_one({"project_id": project["_id"], "_id": item_id})
    if not task:
        return {"message": "no task"}, 404

    data = {"id": task["_id"],
            "title": task["title"],
            "name": task["name"],
            "expiry": task["expiry"],
            "action": task["action"]}

    return {"data": [data]}, 200


@router.put("/project/{id}/task{item_id}")
@check_permissions(["write"])
async def put_task_by_id(id,
                         user: Annotated[dict, Depends(current_user)],
                         item_id):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "no project"}, 404
    task = tasks.find_one({"_id": item_id})
    if not task:
        return {"message": "no task"}, 404
    update = {"$set": {"action": True, "date_complete": datetime.now()}}
    updated = task.update_one({"_id": item_id}, update)
    if updated.raw_result["updatedExisting"]:
        task_true = tasks.find_one({"_id": item_id})
        data = {"id": task_true["_id"],
                "title": task_true["title"],
                "name": task_true["name"],
                "expiry": task_true["expiry"],
                "action": task_true["action"]}
        return data, 201
    return {"message": "error"}, 400


@router.delete("/project/{id}/task/{item_id}")
@check_permissions(["write"])
async def delete_task_by_id(id,
                            user: Annotated[dict, Depends(current_user)],
                            item_id):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})

    if not project:
        return {"message": "no project"}, 404

    task = tasks.find_one({"project_id": item_id})
    if not task:
        return {"message": "no task"}, 404
    task.delete_one({"project_id": item_id})
    return {"message": "deleted"}, 200
