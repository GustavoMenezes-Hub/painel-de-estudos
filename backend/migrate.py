import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conexao = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conexao.cursor()

pasta_migations = "migrations"
arquivos = sorted(os.listdir(pasta_migations))
for arquivo in arquivos:
    if arquivo.endswith(".sql"):
        caminho = os.path.join(pasta_migations, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            sql = f.read()
            print(f"Executando migração: {arquivo}")
            cursor.execute(sql)

conexao.commit()
cursor.close()
conexao.close()
print("migrations concluídas.")