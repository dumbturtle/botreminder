
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import connect_settings

Base = declarative_base()
database_engine = create_engine(connect_settings.DATABASE)
database_Session = sessionmaker(bind=database_engine)
database_session = database_Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegramm_user_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)

    def __init__(self, telegramm_user_id, first_name, last_name, username,
                 chat_id):
        self.telegramm_user_id = telegramm_user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.chat_id = chat_id

    def __repr__(self):
        return "<User {}, {}, {}, {}, {}, {}>".format(
            self.id, self.telegramm_user_id, self.first_name,
            self.last_name,self.username, self.chat_id)


class ReminderData(Base):
    __tablename__ = 'remainders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    comment = Column(String)
    date_remind = Column(DateTime)
    status = Column(String)

    def __init__(self, user_id, comment, date_remind, status):
        self.user_id = user_id
        self.comment = comment
        self.date_remind = date_remind
        self.status = status

    def __repr__(self):
        return "<Data {}, {}, {}, {}, {}>".format(
            self.id, self.user_id, self.comment,
            self.date_remind, self.status)
