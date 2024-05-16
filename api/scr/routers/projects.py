from datetime import datetime
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, Body

from api.middleware.authentication import current_user
from api.schema.schema_project import ProjectPayload, ProjectParams
from db.session import projects, tasks
from handlers.params import filtering
from tasks import send_mail_delete
from api.middleware.authorization import check_permissions
router = APIRouter()


# GROUP_PROJECT
@router.post("/project")
@check_permissions(["write"])
async def create_project(payload: Annotated[ProjectPayload, Body(embed=True)],
                         user: Annotated[dict, Depends(current_user)]):
    try:
        new_project = {"_id": str(ObjectId()), "user_id": user["user_id"], "name": payload.name, "action": False,
                       "created": datetime.now()}
        projects.insert_one(new_project)
    except Exception:
        return {"message": "Error"}
    data = {"name": new_project["name"], "action": new_project["action"]}
    return data, 201


@router.get("/project")
@check_permissions(["read"])
async def get_project(user: Annotated[dict, Depends(current_user)],
                      query_params: Annotated[ProjectParams, Depends()]):
    print(query_params)
    filters = {"user_id": user["user_id"]}
    # Pagination
    page = query_params.page
    per_page = query_params.per_page
    offset = (page - 1) * per_page

    # Filtering
    data_fil = {"name": query_params.name, "id": query_params.id, "action": query_params.action}
    for key, value in data_fil.items():
        if value:
            if key == "name":
                data = {key: value}
                filters.update(filtering(data))
            else:
                filters.update({key: value})

    # Sorting
    query = projects
    if query_params.order == "asc":
        query = projects.find(filters).sort(query_params.sort_by, 1).skip(offset).limit(per_page)
    elif query_params.order == "desc":
        query = projects.find(filters).sort(query_params.sort_by, -1).skip(offset).limit(per_page)

    # Result
    result = list(query)
    total = len(list(projects.find(filters).sort(query_params.sort_by, -1)))
    return {"data": [{"name": data["name"], "_id": data["_id"], "action": data["action"]} for data in result],
            "meta": [{"page": page, "per_page": per_page, "total": total}]}, 200


# ITEM_PROJECT
@router.get("/project/{id}")
@check_permissions(["read"])
async def get_project_by_id(id, user: Annotated[dict, Depends(current_user)]):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "invalid"}
    data = {"id": project["_id"], "name": project["name"], "action": project["action"]}
    return {"data": [data]}


@router.put("/project/{id}")
@check_permissions(["write"])
async def put_project_by_id(id, user: Annotated[dict, Depends(current_user)]):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "invalid"}
    new_action = {"$set": {"action": True}}
    update = projects.update_one({"user_id": user["user_id"], "_id": id}, new_action)
    if update.raw_result["updatedExisting"]:
        cr_project = projects.find_one({"user_id": user["user_id"], "_id": id})
        data = {"id": cr_project["_id"], "name": cr_project["name"], "action": cr_project["action"]}
        return data
    return {"message": "error"}


@router.delete("/project/{id}")
@check_permissions(["write"])
async def delete_project_by_id(id, user: Annotated[dict, Depends(current_user)]):
    project = projects.find_one({"user_id": user["user_id"], "_id": id})
    if not project:
        return {"message": "no project"}

    task = tasks.find_one({"project_id": id})
    if task:
        tasks.delete_many({"project_id": "id"})
    projects.delete_one({"user_id": user["user_id"], "_id": id})
    now = datetime.now()
    time = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    data = {"email": user["email"], "username": user["username"], "name": project["name"], "deletion_date": str(time)}
    send_mail_delete.delay(data)
    return {"message": "deleted"}
