from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db import ProductSale

# Create engine and session
engine = create_engine('mysql+pymysql://root:password@localhost/headoffice')
Session = sessionmaker(bind=engine)
session = Session()

# Create new product sale
new_sale = ProductSale(product_id=1234, date='2022-05-09', region='East', product_name='Product A', quantity=10, cost=5.99, tax=1.50, total_sales=71.89)
session.add(new_sale)
session.commit()

# Read a product sale by ID
# sale = session.query(ProductSale).filter_by(id=2).first()
# print(sale.product_name)

# Update a product sale
# sale.total_sales = 100.00
# session.commit()

# Delete a product sale
# sale_to_delete = session.query(ProductSale).filter_by(id=2).first()
# session.delete(sale_to_delete)
# session.commit()
