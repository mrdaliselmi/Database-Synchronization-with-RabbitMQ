from models.db import ProductSale
import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('mysql+pymysql://root:password@localhost/headoffice')
Session = sessionmaker(bind=engine)
Base = declarative_base()

def fetch_data():
    session = Session()
    product_sales = session.query(ProductSale).all()
    session.close()
    return product_sales

def display_data(product_sales):
    # Create a new Tkinter window
    window = tk.Tk()
    window.title('Head Office Database')
    def refresh_data():
        # Refetch data from the database
        product_sales = fetch_data()

        # Clear the current data in the table
        for widget in window.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Add data rows
        for i, sale in enumerate(product_sales):
            tk.Label(window, text=sale.product_id).grid(row=i+1, column=0)
            tk.Label(window, text=sale.date).grid(row=i+1, column=1)
            tk.Label(window, text=sale.region).grid(row=i+1, column=2)
            tk.Label(window, text=sale.product_name).grid(row=i+1, column=3)
            tk.Label(window, text=sale.quantity).grid(row=i+1, column=4)
            tk.Label(window, text=sale.cost).grid(row=i+1, column=5)
            tk.Label(window, text=sale.tax).grid(row=i+1, column=6)
            tk.Label(window, text=sale.total_sales).grid(row=i+1, column=7)

    # Add header row
    tk.Label(window, text='Product ID').grid(row=0, column=0)
    tk.Label(window, text='Date').grid(row=0, column=1)
    tk.Label(window, text='Region').grid(row=0, column=2)
    tk.Label(window, text='Product Name').grid(row=0, column=3)
    tk.Label(window, text='Quantity').grid(row=0, column=4)
    tk.Label(window, text='Cost').grid(row=0, column=5)
    tk.Label(window, text='Tax').grid(row=0, column=6)
    tk.Label(window, text='Total Sales').grid(row=0, column=7)

    # Add refresh button
    tk.Button(window, text="Refresh", command=refresh_data).grid(row=0, column=8)

    # Add data rows
    for i, sale in enumerate(product_sales):
        tk.Label(window, text=sale.product_id).grid(row=i+1, column=0)
        tk.Label(window, text=sale.date).grid(row=i+1, column=1)
        tk.Label(window, text=sale.region).grid(row=i+1, column=2)
        tk.Label(window, text=sale.product_name).grid(row=i+1, column=3)
        tk.Label(window, text=sale.quantity).grid(row=i+1, column=4)
        tk.Label(window, text=sale.cost).grid(row=i+1, column=5)
        tk.Label(window, text=sale.tax).grid(row=i+1, column=6)
        tk.Label(window, text=sale.total_sales).grid(row=i+1, column=7)
    window.mainloop()


if __name__ == '__main__':
    product_sales = fetch_data()
    display_data(product_sales)