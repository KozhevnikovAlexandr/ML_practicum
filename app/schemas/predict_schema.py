import sys
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database.models import Prediction

sys.path.append(str(Path(__file__).resolve().parents[3]))

class PatientData(BaseModel):
    ModelName: str
    N_Days: int
    Drug: str
    Age: int
    Sex: str
    Ascites: str
    Hepatomegaly: str
    Spiders: str
    Edema: str
    Bilirubin: float
    Cholesterol: float
    Albumin: float
    Copper: float
    Alk_Phos: float
    SGOT: float
    Tryglicerides: float
    Platelets: float
    Prothrombin: float
    Stage: int


class PredictionResponce(BaseModel):
    prediction_id: int
    transaction_id: int
    result: str
    some_data: str  
    model_id: int

    @classmethod
    def get_from_db(cls, db_prediction: Prediction):
        responce = PredictionResponce(
            prediction_id=db_prediction.id,
            transaction_id=db_prediction.transaction_id,
            result=db_prediction.result,
            some_data=db_prediction.some_data,
            model_id=db_prediction.model_id
        )
        return responce
