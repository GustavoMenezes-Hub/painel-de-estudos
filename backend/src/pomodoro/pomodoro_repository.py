from src.db_helpers import db_cursor

class PomodoroRepository:

    @staticmethod
    def listar(id_materias=None):
        with db_cursor() as cursor:
            if id_materias:
                cursor.execute(
                    "SELECT * FROM pomodoro WHERE id_materias = %s ORDER BY inicio DESC;",
                    (id_materias,)
                )
            else:
                cursor.execute("SELECT * FROM pomodoro ORDER BY inicio DESC;")
            return cursor.fetchall()

    @staticmethod
    def buscar_por_id(id_pomodoro):
        with db_cursor() as cursor:
            cursor.execute("SELECT * FROM pomodoro WHERE id_pomodoro = %s;", (id_pomodoro,))
            return cursor.fetchone()

    @staticmethod
    def verificar_materia_existe(id_materias):
        with db_cursor() as cursor:
            cursor.execute("SELECT id_materias FROM materias WHERE id_materias = %s;", (id_materias,))
            return cursor.fetchone() is not None

    @staticmethod
    def verificar_anotacao_existe(id_anotacoes):
        if not id_anotacoes:
            return True
        with db_cursor() as cursor:
            cursor.execute("SELECT id_anotacoes FROM anotacoes WHERE id_anotacoes = %s;", (id_anotacoes,))
            return cursor.fetchone() is not None

    @staticmethod
    def criar(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes):
        with db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pomodoro (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes)
            )
            return cursor.fetchone()

    @staticmethod
    def atualizar(id_pomodoro, inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes):
        with db_cursor() as cursor:
            cursor.execute(
                """
                UPDATE pomodoro
                SET inicio = %s, duracao_foco_min = %s, duracao_pausa_min = %s, tipo = %s, concluida = %s, id_materias = %s, id_anotacoes = %s
                WHERE id_pomodoro = %s
                RETURNING *;
                """,
                (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes, id_pomodoro)
            )
            return cursor.fetchone()

    @staticmethod
    def deletar(id_pomodoro):
        with db_cursor() as cursor:
            cursor.execute("DELETE FROM pomodoro WHERE id_pomodoro = %s;", (id_pomodoro,))