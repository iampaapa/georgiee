from .extensions import db 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    dob = db.Column(db.String(75))
    gender = db.Column(db.String(50))
    number = db.Column(db.String(50))
    classOfUser = db.Column(db.String(75))
    voted = db.Column(db.Boolean)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))  #name of candidate
    position = db.Column(db.String(150)) #president, vice-president
    numberVotes = db.Column(db.Integer) #if null, use 0

    
"""
# PostgreSQL database configuration for creating new tables
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://georgette_project_user:xOLCvgOroVw5S4C3BBFbdTdasca4Qts6@dpg-ciuio7liuiedpv0b2prg-a.oregon-postgres.render.com/georgette_project"  # Replace with your PostgreSQL credentials and database details
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True)
    otp_code = Column(String(6))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    dob = Column(String(75))
    gender = Column(String(50))
    number = Column(String(50))
    classOfUser = Column(String(75))
    voted = Column(Boolean)

class Candidate(Base):
    __tablename__ = 'candidate'
    id = Column(Integer, primary_key=True)
    name = Column(String(75))  #name of candidate
    position = Column(String(150)) #president, vice-president
    numberVotes = Column(Integer) #if null, use 0

Base.metadata.create_all(engine)

"""