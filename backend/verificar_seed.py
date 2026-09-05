import sqlite3

conexao = sqlite3.connect("database.db")
print(conexao.execute("SELECT * FROM materias").fetchall())
print(conexao.execute("SELECT * FROM entregas").fetchall())
print(conexao.execute("SELECT * FROM notas").fetchall())