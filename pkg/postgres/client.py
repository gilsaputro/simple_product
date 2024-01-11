from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Database:
    def __init__(self, engine_url):
        self.engine = create_engine(engine_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)