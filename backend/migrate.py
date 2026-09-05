import sqlite3
import os

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

pasta_migations = "migrations"
arquivos = sorted(os.listdir(pasta_migations))
for arquivo in arquivos:
    if arquivo.endswith(".sql"):
        caminho = os.path.join(pasta_migations, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            sql = f.read()
            print(f"Executando migração: {arquivo}")
            cursor.executescript(sql)

conexao.commit()
conexao.close()
print("migrations concluídas.")