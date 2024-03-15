from pathlib import Path
import os
from typing import Union
from fastapi import APIRouter, FastAPI, Depends, Form, HTTPException, Header, Request, File, Response, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dependency_injector.wiring import inject
from database.init_database import init_db
from database.models import Base, Prediction, User
from schemas.auth_schema import UserSchema
from schemas.auth_schema import UserLoginSchema, UserLoginResponseSchema, UserRegisterSchema
from schemas.predict_schema import PatientData, PredictionResponce
from services.auth_service import AuthService, get_auth_service
from services.predict_service import PredictionService, get_prediction_service
from utils.exeptions import NotFoundError
import starlette.status as status
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.init_database import DB_ADDRESS
from utils.security import get_current_user


app = FastAPI()
security = HTTPBasic()

engine = create_engine('sqlite:///{DB_ADDRESS}', echo=True)
async_engine = create_async_engine(f'sqlite+aiosqlite:///{DB_ADDRESS}')
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()

SessionLocal = get_db()

@app.post("/predict")
async def send_data_for_prediction(
    data: PatientData,
    token: str = Header(None)
):
    ps = get_prediction_service()
    user = get_current_user(token)
    prediction_id = await ps.register_prediction(user_id=user.id, model=data.ModelName, file=data)
    result = await ps.get_predictions(prediction_id=prediction_id)
    return result.result


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r") as file:
        content = file.read()
    return content

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse('templates/favicon.ico')


@app.post("/login", response_model=UserLoginResponseSchema)
async def login(user_info: UserLoginSchema, service: AuthService = Depends(get_auth_service)):
    response = await service.login(user_info)
    return response

@app.get("/login")
async def login(request: Request = None, service: AuthService = Depends(get_auth_service)):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/register")
async def register(user_info: UserRegisterSchema, service: AuthService = Depends(get_auth_service), request: Request = None):
    response = await service.register(user_info)
    return {'token': response.access_token}


@app.get("/register")
async def redirect(request: Request = None):
    await get_me()
    return templates.TemplateResponse("register-success.html", {"request": request})


@app.get("/me")
async def get_me(authorization: str):
    return get_current_user(authorization)

import fire
import uvicorn



def start_service(port="81", host="0.0.0.0", resetdb=True):
    host = os.getenv("HOST", host)
    port = int(os.getenv("PORT", port))
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    init_db(drop_all=True)
    fire.Fire(start_service)
