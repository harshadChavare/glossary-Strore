# models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    
    glossary_entries = relationship("Glossary", back_populates="user")
    cart_items = relationship("ProductCartItem", back_populates="user")  # changed here
    purchases = relationship("Purchase", back_populates="user")


class Glossary(Base):
    __tablename__ = "glossary"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(255), index=True)
    definition = Column(String(1000))
    example = Column(String(1000), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="glossary_entries")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)


class ProductCartItem(Base):
    __tablename__ = "product_cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User", back_populates="cart_items")  # changed here
    product = relationship("Product")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    details = Column(String)

    user = relationship("User", back_populates="purchases")
