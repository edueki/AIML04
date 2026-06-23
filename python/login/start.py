from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from services import UserAuthService

def appstarting():
    auth = UserAuthService()

    class Request(BaseModel):
        username: str
        password: str

    app = FastAPI()

    @app.get("/home")
    def welcome():
        return {"message": "Welcome home page!"}

    @app.get("/hello")
    def hello_world():
        return {"message": "another endpoint"}

    @app.post("/login")
    def login(data: Request):
        response = auth.authenticate(data.username, data.password)
        return response


if __name__ == "__main__":
    appstarting()
    uvicorn.run(app, host="0.0.0.0", port=8000)


