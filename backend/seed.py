import sqlite3

conexao = sqlite3.connect("database.db")
with open("seed.sql", "r", encoding="utf-8") as f:
    sql = f.read()
conexao.executescript(sql)
conexao.commit()
conexao.close()
print("Seed executado com sucesso.")