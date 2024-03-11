import sys
from pathlib import Path

from rq.decorators import job

from utils.get_date import get_now
sys.path.append(str(Path(__file__).resolve().parents[2]))

from repository.user_repository import UserRepository

from app.utils.exeptions import NotFoundError, DuplicatedError
from repository.base_repository import AbstractRepository
from repository.model_repository import ModelsRepository
from repository.prediction_repository import PredictionsRepository
from repository.user_repository import UserRepository
from repository.billing_repository import BilingRepository


from services.task import predict, q




class PredictionService:
    def __init__(self, prediction_repo: AbstractRepository, models_repo: AbstractRepository,
                 user_repo: AbstractRepository, billing_repo):
        self.prediction_repo: AbstractRepository = prediction_repo()
        self.models_repo: AbstractRepository = models_repo()
        self.user_repo: AbstractRepository = user_repo()
        self.billing_repo: AbstractRepository = billing_repo()

    @job("default", timeout=-1)
    def enqueue_predict_task(self, data, *args, **kwargs):
        return predict(data, *args, **kwargs)

    async def register_prediction(self, user_id: int, model: str, file, **kwargs):
        db_model = await self.models_repo.find_by_options(name=model, unique=True)
        db_user = await self.user_repo.find_by_options(id=user_id, unique=True)

        if db_model is None:
            raise NotFoundError(detail="Model not found")

        #if db_user.balance < db_model.price:
        #    raise DuplicatedError(detail="Not enough money")

        #await self.user_repo.update({"balance": db_user.balance - db_model.price}, id=user_id)
        
        billing_data = {}
        billing_data['user_id'] = db_user.id
        billing_data['price'] = db_model.price
        billing_id = await self.billing_repo.add(data=billing_data)
        

        prediction_data = {}
        prediction_data["model_id"] = db_model.id
        prediction_data['transaction_id'] = billing_id
        prediction_data['result'] = 'None'
        prediction_id = await self.prediction_repo.add(data=prediction_data)

        columns_to_predict = ['N_Days', 'Drug', 'Age', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema', 'Bilirubin', 'Cholesterol', 
                              'Albumin', 'Copper', 'Alk_Phos', 'SGOT', 'Tryglicerides', 'Platelets', 'Prothrombin', 'Stage']

        data = {}
        for column in columns_to_predict:
            if column in vars(file):
                data[column] = vars(file)[column]
            else:
                raise NotFoundError(detail=f"Not enough data {column, file}")

        await self.enqueue_predict_task(data, prediction_id, db_model.name, db_model.price, db_user.id, db_user.balance, **kwargs)


        return prediction_id

    async def get_predictions(self, user_id: int, prediction_id: int = None):
        if prediction_id is None:
            predictions = await self.prediction_repo.find_by_options(user_id=user_id)
        else:
            predictions = await self.prediction_repo.find_by_options(id=prediction_id,
                                                                     user_id=user_id,
                                                                     unique=True)
        return predictions


def get_prediction_service():
    return PredictionService(prediction_repo=PredictionsRepository, models_repo=ModelsRepository,
                             user_repo=UserRepository, billing_repo=BilingRepository)