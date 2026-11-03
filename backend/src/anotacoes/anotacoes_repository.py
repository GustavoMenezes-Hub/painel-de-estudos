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
    def vinculada_a_pomodoro_de_outra_materia(id_anotacoes, id_materias, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pomodoro p "
                "JOIN anotacoes a ON a.id_anotacoes = p.id_anotacoes "
                "JOIN materias m ON m.id_materias = a.id_materias "
                "WHERE a.id_anotacoes = %s AND p.id_materias <> %s "
                "AND m.id_usuarios = %s LIMIT 1",
                (id_anotacoes, id_materias, id_usuario),
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
    def atualizar(id_anotacoes, texto, situacao, id_materias, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "UPDATE anotacoes a "
                "SET texto = %s, situacao = %s, id_materias = %s "
                "WHERE a.id_anotacoes = %s "
                "AND EXISTS (SELECT 1 FROM materias origem "
                "WHERE origem.id_materias = a.id_materias AND origem.id_usuarios = %s) "
                "AND EXISTS (SELECT 1 FROM materias destino "
                "WHERE destino.id_materias = %s AND destino.id_usuarios = %s) "
                "AND NOT EXISTS (SELECT 1 FROM pomodoro p "
                "WHERE p.id_anotacoes = a.id_anotacoes AND p.id_materias <> %s) "
                "RETURNING a.*",
                (texto, situacao, id_materias, id_anotacoes, id_usuario,
                 id_materias, id_usuario, id_materias),
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