from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from flask import g

load_dotenv()

engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()