from src.db_helpers import db_cursor

class AnotacoesRepository:
    
    @staticmethod
    def listar(id_materias=None):
        with db_cursor() as cursor:
            if id_materias:
                cursor.execute(
                    "SELECT * FROM anotacoes WHERE id_materias = %s ORDER BY data_criacao DESC;",
                    (id_materias,)
                )
            else:
                cursor.execute("SELECT * FROM anotacoes ORDER BY data_criacao DESC;")
            return cursor.fetchall()

    @staticmethod
    def buscar_por_id(id_anotacoes):
        with db_cursor() as cursor:
            cursor.execute("SELECT * FROM anotacoes WHERE id_anotacoes = %s;", (id_anotacoes,))
            return cursor.fetchone()

    @staticmethod
    def verificar_materia_existe(id_materias):
        with db_cursor() as cursor:
            cursor.execute("SELECT id_materias FROM materias WHERE id_materias = %s;", (id_materias,))
            return cursor.fetchone() is not None

    @staticmethod
    def criar(texto, situacao, id_materias):
        with db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO anotacoes (texto, situacao, id_materias)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (texto, situacao, id_materias)
            )
            return cursor.fetchone()

    @staticmethod
    def atualizar(id_anotacoes, texto, situacao, id_materias):
        with db_cursor() as cursor:
            cursor.execute(
                """
                UPDATE anotacoes
                SET texto = %s, situacao = %s, id_materias = %s
                WHERE id_anotacoes = %s
                RETURNING *;
                """,
                (texto, situacao, id_materias, id_anotacoes)
            )
            return cursor.fetchone()

    @staticmethod
    def deletar(id_anotacoes):
        with db_cursor() as cursor:
            cursor.execute("DELETE FROM anotacoes WHERE id_anotacoes = %s;", (id_anotacoes,))