from src.db_helpers import db_cursor, registro_json

def find_all():
    with db_cursor() as cursor:
        cursor.execute("SELECT id_usuarios, nome FROM usuarios ORDER BY id_usuarios")
        return [registro_json(linha) for linha in cursor.fetchall()]

def find_by_id(id_usuario):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id_usuarios, nome, email, data_criacao FROM usuarios WHERE id_usuarios = %s",
            (id_usuario,),
        )
        return registro_json(cursor.fetchone())

def find_by_email(email):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT id_usuarios, nome, email, senha_hash FROM usuarios WHERE lower(email) = %s",
            (email,),
        )
        return registro_json(cursor.fetchone())

def create(nome, email, senha_hash):
    with db_cursor() as cursor:
        cursor.execute(
            """INSERT INTO usuarios (nome, email, senha_hash)
               VALUES (%s, %s, %s)
               RETURNING id_usuarios, nome, email, data_criacao""",
            (nome, email, senha_hash),
        )
        return registro_json(cursor.fetchone())

def update(id_usuario, campos):
    permitidos = {"nome", "email", "senha_hash"}
    if not campos or not set(campos).issubset(permitidos):
        raise ValueError("Campos inválidos para atualização")
    definicoes = ", ".join(f"{coluna} = %s" for coluna in campos)
    parametros = list(campos.values()) + [id_usuario]
    with db_cursor() as cursor:
        cursor.execute(
            "UPDATE usuarios SET " + definicoes +
            " WHERE id_usuarios = %s RETURNING id_usuarios, nome, email, data_criacao",
            parametros,
        )
        return registro_json(cursor.fetchone())

def delete(id_usuario):
    with db_cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id_usuario,))
        return cursor.rowcount > 0
