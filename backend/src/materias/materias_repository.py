from src.materias.materias_entity import Materia
from src.db import get_connection

def find_all():
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_materias, nome, descricao, data_criacao, id_usuarios " "FROM materias ORDER BY id_materias")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [Materia.from_row(linha) for linha in linhas]

def find_by_id(id_materias):
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_materias, nome, descricao, data_criacao, id_usuarios " "FROM materias WHERE id_materias = %s", (id_materias,))
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()
    return Materia.from_row(linha) if linha else None

def create(nome, descricao, id_usuarios):
    conexao = get_connection()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO materias (nome, descricao, id_usuarios) VALUES (%s, %s, %s) RETURNING id_materias, nome, descricao, data_criacao, id_usuarios", (nome, descricao, id_usuarios))
    linha = cursor.fetchone()
    conexao.commit()
    cursor.close()
    conexao.close()
    return Materia.from_row(linha)

def update(id_materias, nome, descricao):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE materias SET nome = %s, descricao = %s WHERE id_materias = %s RETURNING id_materias, nome, descricao, data_criacao, id_usuarios", (nome, descricao, id_materias))
        linha = cursor.fetchone()
        conexao.commit()
        cursor.close()
    finally:
        conexao.close()
    return Materia.from_row(linha) if linha else None

def delete(id_materias):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM materias WHERE id_materias = %s RETURNING id_materias", (id_materias,))
        linha = cursor.fetchone()
        conexao.commit()
        cursor.close()
    finally:
        conexao.close()
    return True if linha else False