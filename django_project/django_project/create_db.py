import psycopg2
import environ

env = environ.Env()
environ.Env.read_env()

conn = psycopg2.connect(
   database='postgres', user=env('DB_USER'), password=env('DB_PASSWORD'), host=env('DB_HOST'), port=env('DB_PORT')
)
conn.autocommit = True
cursor = conn.cursor()

sql = f"CREATE DATABASE {env('DB_NAME')}"

cursor.execute(sql)
print("Database created successfully........")

conn.close()
