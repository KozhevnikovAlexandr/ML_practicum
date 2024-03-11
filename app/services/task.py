import sys

from pathlib import Path

import redis
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


MODELS_PATH = Path("models")
MODELS_MAP = {
    'Desition Tree': TreeModel(),
    'KNNModel': KNNModel(),
    'boosting': BoostingModel()
}
engine = create_engine(f'sqlite:///{DB_ADDRESS}')

redis_conn = redis.Redis(host='localhost', port=6379)
q = Queue(connection=redis_conn)

async def predict(data, prediction_id, model_name, user_id, user_balance, *args, **kwargs):
    #try:
     #   model = MODELS_MAP[model_name]

        # Load the CSV file into a DataFrame
    model = MODELS_MAP[model_name]
    output = model.predict(pd.DataFrame([data])).argmax()

    update_data = {"result": str(output)}
    update_data = {"result": 5}

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([
        Prediction(result=5)
    ])

    #asyncio.create_task(PredictionsRepository().update(data=update_data, id=prediction_id))
   # except Exception as e:
    #    print(e)

   #     asyncio.create_task(UserRepository().update(data={"balance": user_balance}, id=user_id))
   #
   # asyncio.create_task(PredictionsRepository().update(data=update_data, id=prediction_id))