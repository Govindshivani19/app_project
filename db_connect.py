from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os
local = True
Base = declarative_base()
engine = create_engine('postgresql://%s:%s@%s:5432/%s' %
                       (os.environ['user'],
                        os.environ['password'],
                        os.environ['host'],
                        os.environ['db']
                        ),
                       pool_pre_ping=True, pool_size=30, max_overflow=100)

Session = sessionmaker(bind=engine, autoflush=False)