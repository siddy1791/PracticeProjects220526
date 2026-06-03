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
import os
from dotenv import load_dotenv

load_dotenv()

def db_connection(dbname):
    try:
        # Retrieve credentials securely with safe default fallbacks
        dbms = os.environ.get("DB_DBMS", "postgresql")
        connectionlib = os.environ.get("DB_LIB", "psycopg2")
        username = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        hostname = os.environ.get("DB_HOST", "localhost")
        port = os.environ.get("DB_PORT", "5432")

        if not username or not password:
           raise ValueError("Database credentials missing from environment variables!")
         
        print(f"Connecting to db::{dbname} on {hostname}.{port}")

        engine = create_engine(f"{dbms}+{connectionlib}://{username}:{password}@{hostname}:{port}/{dbname}")
        
        # 2. Establish an explicit connection boundary
        with engine.connect() as conn:
            # We pass the active connection 'conn' instead of the global pool 'engine'
            sql_df = pd.read_sql("select * from orders;",conn)
        
        # 3. Dispose of the engine pool to free up system network sockets completely
        engine.dispose()
        return sql_df

    except Exception as e:
        print(f"Database connection failed due to err: {e}")
        raise e
    
    
