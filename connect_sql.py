import psycopg2
from psycopg2 import Error
import os

class pgSQL():
    # def __init__(self, user, password, host, port, database):

    def __init__(self):
        self.user = 'ramhajdvwdhzto'
        self.password = '514e71430a6f4196a888f40cf2a0f159b4a3341046d59a95b9212688ebb6159c'
        self.host = 'ec2-34-197-141-7.compute-1.amazonaws.com'
        self.port = '5432'
        self.database = 'd2m3452qrqmo7f'
        self.connection = psycopg2.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      database=self.database)
        self.cursor = self.connection.cursor()
    def connectSQL(pgSQL):
        try:
            print ( pgSQL.connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            pgSQL.cursor.execute("SELECT version();")
            record = pgSQL.cursor.fetchone()
            print("You are connected to - ", record,"\n")

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)


    def buildsheet(pgSQL):
        try:
            pgSQL.cursor = pgSQL.connection.cursor()
            create_table_query = '''CREATE TABLE mobile
            (ID INT PRIMARY KEY     NOT NULL,
            MODEL           TEXT    NOT NULL,
            PRICE         REAL); '''
            pgSQL.cursor.execute(create_table_query)
            pgSQL.connection.commit()
            print("Table created successfully in PostgreSQL ")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
    def closedlink(pgSQL):
        pgSQL.cursor.close()
        pgSQL.connection.close()
        print("PostgreSQL connection is closed")


