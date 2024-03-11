from pathlib import Path
import os

from fastapi import FastAPI, Depends, Form, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from database.init_database import init_db
from database.models import Prediction, User
from schemas.predict_schema import PatientData
from services.predict_service import PredictionService, get_prediction_service

app = FastAPI()
security = HTTPBasic()

engine = create_engine('sqlite:///database.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/predict")
async def send_data_for_prediction(
    data: PatientData,
    db: SessionLocal = Depends(get_db),  # type: ignore 
):
    '''
    Prediction request endpoint
    '''
    ps = get_prediction_service()
    prediction_id = await ps.register_prediction(user_id=1, model=data.ModelName, file=data)
    result = db.query(Prediction).filter_by(id=prediction_id).first().result
    return result

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r") as file:
        content = file.read()
    return content

@app.get("/favicon.ico")
async def favicon():
    return FileResponse('templates/index.html')

@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=email, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return "<h1>Welcome to our service!</h1>"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.username, User.password == credentials.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user

import fire
import uvicorn



def start_service(port="81", host="0.0.0.0", resetdb=True):
    host = os.getenv("HOST", host)
    port = int(os.getenv("PORT", port))
    #if resetdb:
    init_db(drop_all=True)  
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    init_db(drop_all=True)
    fire.Fire(start_service)
