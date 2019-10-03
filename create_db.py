from db import Base
from sqlalchemy import create_engine


engine = create_engine("sqlite:///bot_db.db")

##Создание_таблиц
Base.metadata.create_all(engine)