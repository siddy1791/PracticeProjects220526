import psycopg2

# --- > NORMAL DB CONNECTION TO POSTGRES DB <-------------
# def db_connection():
#     try:
#         with psycopg2.connect(dbname="project1",user='admin',password='postgres123',host='localhost',port=5432) as conn:
#             cur = conn.cursor()
#             cur.execute("select version();")
#             version = cur.fetchall()
#             print(version)
#             cur.close()
#             return version
#     except Exception as e:
#         raise e
    

# print(db_connection())

# if __name__=='__main__':
#     print("Attempting to connect to the database...")
#     connect = db_connection()




#  >>>>>>>>>>>>> USING SQLALCHEMY AND PANDAS <<<<<<<<<<<<<<<<<<<<<<<<<<<
import pandas as pd
from sqlalchemy import create_engine

def db_connection(dbms,connectionlib,username,password,hostname,port,dbname):
    try:
        print(f"Connecting to db::{dbname}")
        engine = create_engine(f"{dbms}+{connectionlib}://{username}:{password}@{hostname}:{port}/{dbname}")
        sql_df = pd.read_sql("select * from orders;",engine)
        # sql_df.isnull().sum()  # null check per column
        # sql_df[sql_df.isnull().any(axis=1)] # filter out rows where any column is null. if u want all coulmn null row then replace 'any' with 'all'
        # sql_df[sql_df.duplicated()]  # By default, it checks all columns together. and sees if previous record is same as current
        # sql_df[sql_df['total_amount'] > 50000]
        return sql_df

    except Exception as e:
        raise e
    
if __name__ == '__main__':
    connection = db_connection('postgresql','psycopg2','admin','postgres123','localhost','5432','project1')
    print(connection)
    
