# import os
# import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine

import settings.connect_settings
from database.modeldb import Base


engine = create_engine(settings.connect_settings.DATABASE)

Base.metadata.create_all(engine)