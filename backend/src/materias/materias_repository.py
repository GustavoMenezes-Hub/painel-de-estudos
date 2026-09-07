from src.db import get_connection

def find_all():
    conexao = get_connection()
    cursor = conexao.execute("SELECT id, nome, icone, criado_em FROM materias")
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(linha) for linha in linhas]
