from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from datetime import datetime

#create model class
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True)
    username = Column(String(50), nullable=False)
    email =Column(String(64),nullable=False)
    password =Column(String(64),nullable=False)
    created_at =Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.username
    

class File(Base):
     __tablename__ = 'files'
     id = Column(Integer, primary_key=True)
     path = Column(String(255), nullable=False)
     user_id = Column(Integer, ForeignKey('users.id'))
     created_at = Column(DateTime, default=datetime.now)

#more classes for other tables
     
#utility functions
def open_db():
        engine = create_engine('sqlite:///project.db',echo=True)
        session = sessionmaker(bind=engine)
        return session()
def add_to_db(object):
     db = open_db()
     db.add(object)
     db.commit()
     db.close()

if __name__=="__main__":
    ##create engine
    engine = create_engine('sqlite:///project.db',echo=True)
    Base.metadata.create_all(engine)


