from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(70), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user") # one to many

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    ORDER_STATUS = (
        ('Pending', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('delivered', 'Delivered')
    )
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(
        ChoiceType(ORDER_STATUS),
        default='Pending'
    )
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")  # many to one
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)
    price = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name}>"