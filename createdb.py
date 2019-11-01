from sqlalchemy import create_engine

import settings.connect_settings
from database.modeldb import Base


engine = create_engine(settings.connect_settings.DATABASE)

##Создание_таблиц
Base.metadata.create_all(engine)