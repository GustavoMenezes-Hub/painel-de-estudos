from src.materias.materias_entity import Materia
from src.db import get_connection

def find_all(id_usuario):
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id_materias, nome, descricao, data_criacao, id_usuarios "
                "FROM materias WHERE id_usuarios = %s ORDER BY id_materias",
                (id_usuario,),
            )
            linhas = cursor.fetchall()
    finally:
        conexao.close()
    return [Materia.from_row(linha) for linha in linhas]

def find_by_id(id_materias, id_usuario):
    conexao = get_connection()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id_materias, nome, descricao, data_criacao, id_usuarios "
                "FROM materias WHERE id_materias = %s AND id_usuarios = %s",
                (id_materias, id_usuario),
            )
            linha = cursor.fetchone()
    finally:
        conexao.close()
    return Materia.from_row(linha) if linha else None

def create(nome, descricao, id_usuario):
    conexao = get_connection()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO materias (nome, descricao, id_usuarios) "
                    "VALUES (%s, %s, %s) "
                    "RETURNING id_materias, nome, descricao, data_criacao, id_usuarios",
                    (nome, descricao, id_usuario),
                )
                linha = cursor.fetchone()
    finally:
        conexao.close()
    return Materia.from_row(linha)

def update(id_materias, nome, descricao, id_usuario):
    conexao = get_connection()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "UPDATE materias SET nome = %s, descricao = %s "
                    "WHERE id_materias = %s AND id_usuarios = %s "
                    "RETURNING id_materias, nome, descricao, data_criacao, id_usuarios",
                    (nome, descricao, id_materias, id_usuario),
                )
                linha = cursor.fetchone()
    finally:
        conexao.close()
    return Materia.from_row(linha) if linha else None

def delete(id_materias, id_usuario):
    conexao = get_connection()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM materias WHERE id_materias = %s AND id_usuarios = %s "
                    "RETURNING id_materias",
                    (id_materias, id_usuario),
                )
                linha = cursor.fetchone()
    finally:
        conexao.close()
    return linha is not None