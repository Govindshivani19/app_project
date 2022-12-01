from sqlalchemy import ARRAY, BigInteger, Boolean, Column, Date, DateTime, \
    Integer, \
    Numeric, SmallInteger, String, text, JSON, Float, TIMESTAMP, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, nullable=False, server_default=text("nextval('user_id_seq'::regclass)"))
    email = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False, server_default=text("app User"))
    last_name = Column(String(100), nullable=False, server_default=text("app User"))
    password = Column(String(200), nullable=False, server_default=text("null"))


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, nullable=False, server_default=text("nextval('products_id_seq'::regclass)"))
    category_name = Column(String(100), nullable=False)
    product_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=False)
    discounted_percentage = Column(Integer, nullable=False)
    image_url = Column(String(100), nullable=False)
    inventory_category_data = Column(JSON, nullable=True)


class Ordered_info(Base):
    __tablename__ = 'ordered_info'
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, nullable=False, server_default=text("nextval('ordered_info_id_seq'::regclass)"))
    user_id = Column(Integer, nullable=False)
    ordered_data = Column(JSON, nullable=True)
