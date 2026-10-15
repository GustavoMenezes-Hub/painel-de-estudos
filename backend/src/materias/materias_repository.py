from src.db import get_connection

def find_all():
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_materias, nome, descricao, data_criacao, id_usuarios " "FROM materias ORDER BY id_materias")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [dict(linha) for linha in linhas]
