from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

engine = create_engine('mysql+pymysql://root:password@localhost/headoffice')

Base = declarative_base()

class ProductSale(Base):
    __tablename__ = 'product_sales'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    date = Column(Date)
    region = Column(String(50))
    product_name = Column(String(50))
    quantity = Column(Integer)
    cost = Column(Float)
    tax = Column(Float)
    total_sales = Column(Float)
    
    def __init__(self, product_id, date, region, product_name, quantity, cost, tax, total_sales):
        self.product_id = product_id
        self.date = date
        self.region = region
        self.product_name = product_name
        self.quantity = quantity
        self.cost = cost
        self.tax = tax
        self.total_sales = total_sales
    
Base.metadata.create_all(engine)
