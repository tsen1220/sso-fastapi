from fastapi import FastAPI
import uvicorn
from fastapi import Depends
from repositories.user_repository import UserRepository, get_user_repository

app = FastAPI()

@app.get("/")
def read_root(repo: UserRepository = Depends(get_user_repository)):
    return repo.get_users()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)