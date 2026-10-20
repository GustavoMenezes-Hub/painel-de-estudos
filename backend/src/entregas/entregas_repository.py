from src.db_helpers import db_cursor, registro_json

_CAMPOS = "e.id_entregas, e.titulo, e.data_vencimento, e.data_criacao, e.situacao, e.id_materias"

def materia_do_usuario(id_materia, id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM materias WHERE id_materias = %s AND id_usuarios = %s",
            (id_materia, id_usuario),
        )
        return cursor.fetchone() is not None

def find_all(id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT " + _CAMPOS +
            " FROM entregas e JOIN materias m ON m.id_materias = e.id_materias"
            " WHERE m.id_usuarios = %s ORDER BY e.id_entregas",
            (id_usuario,),
        )
        return [registro_json(linha) for linha in cursor.fetchall()]

def find_by_id(id_entrega, id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT " + _CAMPOS +
            " FROM entregas e JOIN materias m ON m.id_materias = e.id_materias"
            " WHERE e.id_entregas = %s AND m.id_usuarios = %s",
            (id_entrega, id_usuario),
        )
        return registro_json(cursor.fetchone())

def create(titulo, data_vencimento, situacao, id_materia):
    with db_cursor() as cursor:
        cursor.execute(
            """INSERT INTO entregas (titulo, data_vencimento, situacao, id_materias)
               VALUES (%s, %s, %s, %s)
               RETURNING id_entregas, titulo, data_vencimento, data_criacao, situacao, id_materias""",
            (titulo, data_vencimento, situacao, id_materia),
        )
        return registro_json(cursor.fetchone())

def update(id_entrega, campos):
    permitidos = {"titulo", "data_vencimento", "situacao", "id_materias"}
    if not campos or not set(campos).issubset(permitidos):
        raise ValueError("Campos inválidos para atualização")
    definicoes = ", ".join(f"{coluna} = %s" for coluna in campos)
    parametros = list(campos.values()) + [id_entrega]
    with db_cursor() as cursor:
        cursor.execute(
            "UPDATE entregas SET " + definicoes +
            " WHERE id_entregas = %s RETURNING id_entregas, titulo, data_vencimento,"
            " data_criacao, situacao, id_materias",
            parametros,
        )
        return registro_json(cursor.fetchone())

def delete(id_entrega):
    with db_cursor() as cursor:
        cursor.execute("DELETE FROM entregas WHERE id_entregas = %s", (id_entrega,))
        return cursor.rowcount > 0