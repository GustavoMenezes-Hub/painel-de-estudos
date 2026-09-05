import sqlite3

conexao = sqlite3.connect("database.db")
tabelas = conexao.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()
print(tabelas)