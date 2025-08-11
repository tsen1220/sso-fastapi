from fastapi import FastAPI
import uvicorn
from fastapi import Depends
from app.routes import user_route
from app.routes.otp_route import otp_route
from app.routes.auth_route import auth_route

app = FastAPI()

app.include_router(user_route)
app.include_router(otp_route)
app.include_router(auth_route)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)