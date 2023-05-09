import sys
import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db import ProductSale
import pika
from constants.branchCredentials import Credentials
# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

engine = create_engine('mysql+pymysql://root:password@localhost/branchoffice1')
Session = sessionmaker(bind=engine) 

class ProductManagementApp:
    def on_closing(self):
        # Close the connection
        connection.close()
        sys.exit(0)
        
    def __init__(self):
        self.session = Session()
        self.product_sales = self.session.query(ProductSale).all()
        self.window = tk.Tk()
        self.window.title("Product Management App - Branch Office 1")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.filepath = 'migration-script.sql'

        # Create labels for each input field
        tk.Label(self.window, text='Product ID').grid(row=0, column=1)
        tk.Label(self.window, text='Date (YYYY-MM-DD)').grid(row=1, column=1)
        tk.Label(self.window, text='Region').grid(row=2, column=1)
        tk.Label(self.window, text='Product Name').grid(row=3, column=1)
        tk.Label(self.window, text='Quantity').grid(row=4, column=1)
        tk.Label(self.window, text='Cost').grid(row=5, column=1)
        tk.Label(self.window, text='Tax').grid(row=6, column=1)
        tk.Label(self.window, text='Total Sales').grid(row=7, column=1)

        # Create input fields for each label
        self.product_id_entry = tk.Entry(self.window)
        self.product_id_entry.grid(row=0, column=2)

        self.date_entry = tk.Entry(self.window)
        self.date_entry.grid(row=1, column=2)

        self.region_entry = tk.Entry(self.window)
        self.region_entry.grid(row=2, column=2)

        self.product_name_entry = tk.Entry(self.window)
        self.product_name_entry.grid(row=3, column=2)

        self.quantity_entry = tk.Entry(self.window)
        self.quantity_entry.grid(row=4, column=2)

        self.cost_entry = tk.Entry(self.window)
        self.cost_entry.grid(row=5, column=2)

        self.tax_entry = tk.Entry(self.window)
        self.tax_entry.grid(row=6, column=2)

        self.total_sales_entry = tk.Entry(self.window)
        self.total_sales_entry.grid(row=7, column=2)

        # Create buttons for add, update, and delete operations
        tk.Button(self.window, text="Add", command=self.add_product).grid(row=8, column=0)
        tk.Button(self.window, text="Update", command=self.update_product).grid(row=8, column=1)
        tk.Button(self.window, text="Delete", command=self.delete_product).grid(row=8, column=2)
        tk.Button(self.window, text="Sync", command=self.sync_with_head_office).grid(row=3, column=3)
        tk.Button(self.window, text="Clear", command=self.clear_input_fields).grid(row=8, column=3)
        tk.Button(self.window, text="Refresh", command=self.refresh_data).grid(row=8, column=4)

        # Create a table to display existing products
        tk.Label(self.window, text='Existing Products').grid(row=9, column=0, columnspan=8)
        tk.Label(self.window, text='Product ID').grid(row=10, column=0)
        tk.Label(self.window, text='Date').grid(row=10, column=1)
        tk.Label(self.window, text='Region').grid(row=10, column=2)
        tk.Label(self.window, text='Product Name').grid(row=10, column=3)
        tk.Label(self.window, text='Quantity').grid(row=10, column=4)
        tk.Label(self.window, text='Cost').grid(row=10, column=5)
        tk.Label(self.window, text='Tax').grid(row=10, column=6)
        tk.Label(self.window, text='Total Sales').grid(row=10, column=7)
        self.table_row_index = 11
        for product_sale in self.product_sales:
            tk.Label(self.window, text=product_sale.id).grid(row=self.table_row_index, column=0)
            tk.Label(self.window, text=str(product_sale.date)).grid(row=self.table_row_index, column=1)
            tk.Label(self.window, text=product_sale.region).grid(row=self.table_row_index, column=2)
            tk.Label(self.window, text=product_sale.product_name).grid(row=self.table_row_index, column=3)
            tk.Label(self.window, text=str(product_sale.quantity)).grid(row=self.table_row_index, column=4)
            tk.Label(self.window, text=str(product_sale.cost)).grid(row=self.table_row_index, column=5)
            tk.Label(self.window, text=str(product_sale.tax)).grid(row=self.table_row_index, column=6)
            tk.Label(self.window, text=str(product_sale.total_sales)).grid(row=self.table_row_index, column=7)
            self.table_row_index += 1

        self.window.mainloop()

    def add_product(self):
        new_product_sale = ProductSale(
            product_id=int(self.product_id_entry.get()),
            date=self.date_entry.get(),
            region="EAST",
            product_name=self.product_name_entry.get(),
            quantity=int(self.quantity_entry.get()),
            cost=float(self.cost_entry.get()),
            tax=float(self.tax_entry.get()),
            total_sales=float(self.total_sales_entry.get())
        )
        # prepare a query to insert a new product into the database
        query = 'INSERT INTO product_sales (product_id, date, region, product_name, quantity, cost, tax, total_sales) VALUES ({0}, "{1}", "{2}", "{3}", {4}, {5}, {6}, {7});'.format(
            new_product_sale.product_id,
            new_product_sale.date,
            "EAST",
            new_product_sale.product_name,
            new_product_sale.quantity,
            new_product_sale.cost,
            new_product_sale.tax,
            new_product_sale.total_sales
        )
        # write query in file
        with open(self.filepath, 'a') as f:
            f.write('\n'+query)
        # print(query)
        self.session.add(new_product_sale)
        self.session.commit()
        self.refresh_data()

    def update_product(self):
        product_id = int(self.product_id_entry.get())
        product_sale = self.session.query(ProductSale).filter_by(id=product_id).first()
        query = 'UPDATE product_sales SET '
        statements = []
        if (self.date_entry.get()):
            product_sale.date = self.date_entry.get()
            statements.append('date = "{0}", '.format(product_sale.date))
        if (self.region_entry.get()):
            product_sale.region = "EAST"
            statements.append('region = "{0}", '.format(product_sale.region))
        if (self.product_name_entry.get()):
            product_sale.product_name = self.product_name_entry.get()
            statements.append('product_name = "{0}", '.format(product_sale.product_name))
        if (self.quantity_entry.get()):
            product_sale.quantity = int(self.quantity_entry.get())
            statements.append('quantity = {0}, '.format(product_sale.quantity))
        if (self.cost_entry.get()):
            product_sale.cost = float(self.cost_entry.get())
            statements.append('cost = {0}, '.format(product_sale.cost))
        if (self.tax_entry.get()):
            product_sale.tax = float(self.tax_entry.get())
            statements.append('tax = {0}, '.format(product_sale.tax))
        if (self.total_sales_entry.get()):
            product_sale.total_sales = float(self.total_sales_entry.get())
            statements.append('total_sales = {0}, '.format(product_sale.total_sales))
        query += ', '.join(statements)
        query += ' WHERE product_id = {0} AND region = "{1}";'.format(product_sale.product_id, "EAST")
        self.session.commit()
        with open(self.filepath, 'a') as f:
            f.write('\n'+query)
        # print(query)
        self.refresh_data()

    def delete_product(self):
        product_id = self.product_id_entry.get()
        product_sale = self.session.query(ProductSale).filter_by(id=product_id).first()
        query = 'DELETE FROM product_sales WHERE product_id = {0} AND region = "{1}";'.format(product_sale.product_id, product_sale.region)
        self.session.delete(product_sale)
        self.session.commit()
        with open(self.filepath, 'a') as f:
            f.write('\n'+query)
        # print(query)
        self.clear_input_fields()
        self.refresh_data()
        
    def refresh_data(self):
        self.product_sales = self.session.query(ProductSale).all()
        for widget in self.window.grid_slaves():
            if int(widget.grid_info()["row"]) > 10:
                widget.destroy()
        self.table_row_index = 11
        for product_sale in self.product_sales:
            tk.Label(self.window, text=product_sale.id).grid(row=self.table_row_index, column=0)
            tk.Label(self.window, text=str(product_sale.date)).grid(row=self.table_row_index, column=1)
            tk.Label(self.window, text=product_sale.region).grid(row=self.table_row_index, column=2)
            tk.Label(self.window, text=product_sale.product_name).grid(row=self.table_row_index, column=3)
            tk.Label(self.window, text=str(product_sale.quantity)).grid(row=self.table_row_index, column=4)
            tk.Label(self.window, text=str(product_sale.cost)).grid(row=self.table_row_index, column=5)
            tk.Label(self.window, text=str(product_sale.tax)).grid(row=self.table_row_index, column=6)
            tk.Label(self.window, text=str(product_sale.total_sales)).grid(row=self.table_row_index, column=7)
            self.table_row_index +=1
    
    def clear_input_fields(self):
        self.product_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.region_entry.delete(0, tk.END)
        self.product_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        self.total_sales_entry.delete(0, tk.END)
    
    def sync_with_head_office(self):
        channel = connection.channel()
        # Declare the exchange and queue to use
        channel.exchange_declare(exchange='headoffice', exchange_type='direct')
        # Read the script.sql file and send every 50 lines separately
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 50):
                message = ''.join(lines[i:i+50])
                try:
                    channel.basic_publish(exchange='headoffice',
                                        routing_key='headoffice',
                                        body=message,
                                        properties=pika.BasicProperties(content_type='text/plain',
                                                            delivery_mode=pika.DeliveryMode.Transient))
                    with open(self.filepath, 'w') as f:
                        f.write('')
                except pika.exceptions.UnroutableError :
                    print('Message was returned, retry to sync with head office later.')



if __name__ == '__main__':
    ProductManagementApp()