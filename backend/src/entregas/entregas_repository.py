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
            f"SELECT {_CAMPOS} "
            "FROM entregas e "
            "JOIN materias m ON m.id_materias = e.id_materias "
            "WHERE m.id_usuarios = %s "
            "ORDER BY e.id_entregas",
            (id_usuario,),
        )
        return [registro_json(linha) for linha in cursor.fetchall()]

def find_by_id(id_entrega, id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            f"SELECT {_CAMPOS} "
            "FROM entregas e "
            "JOIN materias m ON m.id_materias = e.id_materias "
            "WHERE e.id_entregas = %s AND m.id_usuarios = %s",
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

def update(id_entrega, id_usuario, campos):
    permitidos = {"titulo", "data_vencimento", "situacao", "id_materias"}

    if not campos or not set(campos).issubset(permitidos):
        raise ValueError("Campos inválidos para atualização")

    definicoes = ", ".join(f"{coluna} = %s" for coluna in campos)

    parametros = list(campos.values()) + [
        id_entrega,
        id_usuario,
        campos.get("id_materias"),
        id_usuario,
    ]

    with db_cursor() as cursor:
        cursor.execute(
            f"UPDATE entregas e SET {definicoes} "
            "WHERE e.id_entregas = %s "
            "AND EXISTS ("
            "SELECT 1 FROM materias m "
            "WHERE m.id_materias = e.id_materias "
            "AND m.id_usuarios = %s"
            ") "
            "AND EXISTS ("
            "SELECT 1 FROM materias destino "
            "WHERE destino.id_materias = COALESCE(%s, e.id_materias) "
            "AND destino.id_usuarios = %s"
            ") "
            "RETURNING e.id_entregas, e.titulo, e.data_vencimento, "
            "e.data_criacao, e.situacao, e.id_materias",
            parametros,
        )
        return registro_json(cursor.fetchone())

def delete(id_entrega, id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            "DELETE FROM entregas e "
            "WHERE e.id_entregas = %s "
            "AND EXISTS ("
            "SELECT 1 FROM materias m "
            "WHERE m.id_materias = e.id_materias "
            "AND m.id_usuarios = %s"
            ")",
            (id_entrega, id_usuario),
        )
        return cursor.rowcount > 0