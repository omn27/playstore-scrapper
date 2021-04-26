from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///scraper.sqlite",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()