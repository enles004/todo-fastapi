from fastapi import FastAPI
import uvicorn
from api.scr.routers import auth, projects, tasks

app = FastAPI()

if __name__ == "__main__":
    app.include_router(auth.router, prefix="/api", tags=["User"])
    app.include_router(projects.router, prefix="/api", tags=["Project"])
    app.include_router(tasks.router, prefix="/api", tags=["Task"])
    uvicorn.run(app)