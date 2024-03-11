import sys
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

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
