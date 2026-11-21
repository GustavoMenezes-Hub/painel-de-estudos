from src.api_errors import ApiError
from src.db_helpers import db_cursor

class AnotacoesRepository:

    @staticmethod
    def listar(id_usuario, id_materias=None):
        with db_cursor() as cursor:
            if id_materias is not None:
                cursor.execute(
                    "SELECT a.* FROM anotacoes a "
                    "JOIN materias m ON m.id_materias = a.id_materias "
                    "WHERE m.id_usuarios = %s AND a.id_materias = %s "
                    "ORDER BY a.data_criacao DESC",
                    (id_usuario, id_materias),
                )
            else:
                cursor.execute(
                    "SELECT a.* FROM anotacoes a "
                    "JOIN materias m ON m.id_materias = a.id_materias "
                    "WHERE m.id_usuarios = %s ORDER BY a.data_criacao DESC",
                    (id_usuario,),
                )
            return cursor.fetchall()

    @staticmethod
    def buscar_por_id(id_anotacoes, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT a.* FROM anotacoes a "
                "JOIN materias m ON m.id_materias = a.id_materias "
                "WHERE a.id_anotacoes = %s AND m.id_usuarios = %s",
                (id_anotacoes, id_usuario),
            )
            return cursor.fetchone()

    @staticmethod
    def verificar_materia_existe(id_materias, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM materias WHERE id_materias = %s AND id_usuarios = %s",
                (id_materias, id_usuario),
            )
            return cursor.fetchone() is not None

    @staticmethod
    def criar(texto, situacao, id_materias, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "INSERT INTO anotacoes (texto, situacao, id_materias) "
                "SELECT %s, %s, m.id_materias FROM materias m "
                "WHERE m.id_materias = %s AND m.id_usuarios = %s RETURNING *",
                (texto, situacao, id_materias, id_usuario),
            )
            return cursor.fetchone()

    @staticmethod
    def atualizar(id_anotacoes, campos, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT a.* FROM anotacoes a JOIN materias m USING (id_materias) "
                "WHERE a.id_anotacoes = %s AND m.id_usuarios = %s FOR UPDATE OF a",
                (id_anotacoes, id_usuario),
            )
            atual = cursor.fetchone()
            if atual is None:
                return None
            id_materias = campos.get("id_materias", atual["id_materias"])
            if id_materias != atual["id_materias"]:
                cursor.execute(
                    "SELECT 1 FROM pomodoro WHERE id_anotacoes = %s AND id_materias <> %s LIMIT 1",
                    (id_anotacoes, id_materias),
                )
                if cursor.fetchone() is not None:
                    raise ApiError("Anotação vinculada a Pomodoro de outra matéria.", 409)
            cursor.execute(
                "UPDATE anotacoes a SET texto = %s, situacao = %s, id_materias = m.id_materias "
                "FROM materias m WHERE a.id_anotacoes = %s "
                "AND m.id_materias = %s AND m.id_usuarios = %s RETURNING a.*",
                (campos.get("texto", atual["texto"]), campos.get("situacao", atual["situacao"]),
                 id_anotacoes, id_materias, id_usuario),
            )
            return cursor.fetchone()

    @staticmethod
    def deletar(id_anotacoes, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "DELETE FROM anotacoes a WHERE a.id_anotacoes = %s "
                "AND EXISTS (SELECT 1 FROM materias m "
                "WHERE m.id_materias = a.id_materias AND m.id_usuarios = %s) "
                "RETURNING a.id_anotacoes",
                (id_anotacoes, id_usuario),
            )
            return cursor.fetchone() is not None