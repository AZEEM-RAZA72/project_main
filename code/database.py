from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import sessionmaker

#base model class
Base=declarative_base()
#this class is made to create table
class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    username=Column(String(50), nullable=False)
    email=Column(String(64),unique=True)
    password=Column(String(64))
    created_at=Column(DateTime, default=datetime.now)

    def _str_(self):     #to print
        return self.username

#base model class
Base=declarative_base()
#this class is made to create table
class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    username=Column(String(50), nullable=False)
    email=Column(String(64),unique=True)
    password=Column(String(64))
    created_at=Column(DateTime, default=datetime.now)

    def _str_(self):     #to print
        return self.username

   
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(64), unique=True)
    phone = Column(String(13), nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def str(self):
        return self.name


#utility functions
def open_db():
    engine=create_engine('sqlite:///project.db' , echo=True)
    session = sessionmaker(bind=engine)
    return session()

def add_to_db(object):
    db = open_db()
    db = open_db()
    db.add(object)
    db.commit()
    db.close()

if __name__== "__main__":
    #create engine
    engine=create_engine('sqlite:///project.db' , echo=True)
    Base.metadata.create_all(engine) #temporary connection