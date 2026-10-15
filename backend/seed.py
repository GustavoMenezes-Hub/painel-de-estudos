import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conexao = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conexao.cursor()

with open("seed.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)

conexao.commit()
cursor.close()
conexao.close()
print("seed concluído.")