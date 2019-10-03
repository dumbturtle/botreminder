
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
database_engine = create_engine("sqlite:///bot_db.db")
database_Session = sessionmaker(bind=database_engine)
database_session = database_Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)

    def __init__(self, user_id, first_name, last_name, username, chat_id):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.chat_id = chat_id
    
    def __repr__(self):
        return "<User('%d','%s', '%s', '%s', '%d')>" % (self.user_id, self.first_name, self.last_name, self.username, self.chat_id)


'''
class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),index=True)
    text = Column(String)

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
    
    def __repr__(self):
        return "<Data('%s','%s')>" % (self.user_id, self.text)

"user_id": effective_user.id,
"first_name": effective_user.first_name,
"last_name": effective_user.last_name,
"username": effective_user.username,
"chat_id": message.chat_id
'''
def add_user_to_database(database_session, user_id, first_name, last_name, username, chat_id):
        information_about_user = database_session.query(User).filter(User.user_id == user_id).all() 
        if not information_about_user:                
                information_about_user = User(user_id, first_name, last_name, username, chat_id)
                database_session.add(information_about_user)
                try:
                        database_session.commit()
                        return 'Commited'
                except SQLAlchemyError:
                        return 'Error'

        return information_about_user[0].first_name

def delete_user_from_database(database_session, user_id):
        information_about_user = database_session.query(User).filter(User.user_id == user_id).all()

        if not information_about_user:
            return 'No user'

        database_session.query(User).filter(User.user_id == user_id).delete()
        try:
            database_session.commit()
            return 'Commited'
        except SQLAlchemyError:
            return 'Error'

def check_user_in_database(database_session, user_id):
        information_about_user = database_session.query(User).filter(User.user_id == user_id).all()
        
        if not information_about_user:
            return 'No user'
        
        return information_about_user[0].first_name
