import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pika
import mysql.connector

host_args = {
    "host": "localhost",
    "user": "root",
    "password": "password"
}

con = mysql.connector.connect(**host_args)
cur = con.cursor(dictionary=True)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
engine = create_engine('mysql+pymysql://root:password@localhost/headoffice')
Session = sessionmaker(bind=engine)

class synchronization:
    def __init__(self, filepath):
        self.session = Session()
        self.filepath = filepath

    def synchronize(self):
        with open(self.filepath, 'r') as sql_file:
            result_iterator = cur.execute(sql_file.read(), multi=True)
            for res in result_iterator:
                print("Running query: ", res)
                print(f"Affected {res.rowcount} rows" )
        con.commit()
        # with engine.connect() as con:
        #     with open(self.filepath) as file:
        #         query = text(file.read())
        #         print(query)
        #         con.execute(query)
        with open(self.filepath, 'w') as file:
            file.write('')

    def receive_messages(self):
        
        channel = connection.channel()
        # Declare a queue to receive messages
        queue = channel.queue_declare(queue='headoffice')
        queue_name = queue.method.queue
        channel.queue_bind(exchange='headoffice',
                            queue=queue_name,
                            routing_key='headoffice')
        
        def callback(ch, method, properties, body):
            print(" [x] Received migration script")
            with open(self.filepath, 'a') as f:
                # Write the SQL statement to the file
                # message = json.loads(body)
                message = body.decode('utf-8')
                message = "USE headoffice;\n"+message
                f.write(message + '\n')
            self.synchronize()
        
        channel.basic_consume(queue='headoffice', on_message_callback=callback, auto_ack=True)
        
        print(' [*] Waiting for messages. To exit press CTRL+C')
        # Start consuming messages
        channel.start_consuming()

        # Close the connection
        connection.close()
if __name__ == '__main__':
    sync = synchronization('received_sql_script.sql')
    try:
        sync.receive_messages()
    except KeyboardInterrupt:
        print('Interrupted')