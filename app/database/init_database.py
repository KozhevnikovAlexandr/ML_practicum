import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import IntegrityError

sys.path.append(str(Path(__file__).resolve().parents[2]))
from database.models import Base, Model

DB_ADDRESS = 'database.db'

engine = create_engine(f'sqlite:///{DB_ADDRESS}')

def init_db(engine=engine, drop_all=True):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
        # Создаем несколько записей моделей, если они еще не существуют
    session.add_all([
        Model(name='tree', price=5),
        Model(name='knn', price=10),
        Model(name='boosting', price=15)
    ])
    session.commit()
    
    session.close()