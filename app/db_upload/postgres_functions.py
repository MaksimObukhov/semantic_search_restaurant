import psycopg2
from fastapi import HTTPException
from psycopg2 import extras
from sqlalchemy import create_engine
import pandas as pd


class PostgresFunctions:
    def __init__(self, user, password, host, port, dbname):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

    def create_connection(self):
        connection_string = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}'
        engine = create_engine(connection_string)
        return engine

    def upload_data(self, engine, table_name, csv_file):
        with engine.connect() as connection:
            if connection.dialect.has_table(connection, table_name):
                connection.execute(f'DROP TABLE IF EXISTS {table_name}')

            df = pd.read_csv(csv_file)
            df.to_sql(table_name, engine, index=False, if_exists='replace')

    def get_businesses(self, table_name, business_id):
        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname)

            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = f"SELECT * FROM {table_name} WHERE business_id = %s"
            cursor.execute(query, (business_id,))
            table_info = cursor.fetchone()

            cursor.close()
            conn.close()

            return table_info

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying PostgreSQL: {str(e)}")
