import sys

from pathlib import Path

import asyncio
from rq import Queue
import pandas as pd
from sqlalchemy import create_engine
from database.init_database import DB_ADDRESS
from database.models import Prediction
sys.path.append(str(Path(__file__).resolve().parents[1]))
from ml.tree_model import TreeModel, KNNModel, BoostingModel
from app.repository.prediction_repository import PredictionsRepository
from app.repository.user_repository import UserRepository
from sqlalchemy.orm import sessionmaker
from app.utils.exeptions import NotFoundError, DuplicatedError


MODELS_PATH = Path("models")
MODELS_MAP = {
    'tree': TreeModel(),
    'knn': KNNModel(),
    'boosting': BoostingModel()
}


from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

sync_engine = create_engine(f'sqlite:///{DB_ADDRESS}')
async_engine = create_async_engine(f'sqlite+aiosqlite:///{DB_ADDRESS}')
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def predict(data, prediction_id, model_name, *args, **kwargs):
    model = MODELS_MAP[model_name]

    output = int(model.predict(pd.DataFrame.from_dict([data])).argmax())

    await asyncio.create_task(PredictionsRepository().update(data={'result': output}, id=prediction_id))