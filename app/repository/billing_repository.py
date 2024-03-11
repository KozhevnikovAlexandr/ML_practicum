import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from repository.base_repository import SQLAlchemyRepository
from database.models import BillingHistory

class BilingRepository(SQLAlchemyRepository):
    model = BillingHistory