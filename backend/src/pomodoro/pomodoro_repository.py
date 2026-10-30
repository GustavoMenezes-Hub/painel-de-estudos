from src.db_helpers import db_cursor

class PomodoroRepository:

    @staticmethod
    def listar(id_usuario, id_materias=None):
        with db_cursor() as cursor:
            if id_materias is not None:
                cursor.execute(
                    "SELECT p.* FROM pomodoro p "
                    "JOIN materias m ON m.id_materias = p.id_materias "
                    "WHERE m.id_usuarios = %s AND p.id_materias = %s "
                    "ORDER BY p.inicio DESC",
                    (id_usuario, id_materias),
                )
            else:
                cursor.execute(
                    "SELECT p.* FROM pomodoro p "
                    "JOIN materias m ON m.id_materias = p.id_materias "
                    "WHERE m.id_usuarios = %s ORDER BY p.inicio DESC",
                    (id_usuario,),
                )
            return cursor.fetchall()

    @staticmethod
    def buscar_por_id(id_pomodoro, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT p.* FROM pomodoro p "
                "JOIN materias m ON m.id_materias = p.id_materias "
                "WHERE p.id_pomodoro = %s AND m.id_usuarios = %s",
                (id_pomodoro, id_usuario),
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
    def verificar_anotacao_existe(id_anotacoes, id_materias, id_usuario):
        if id_anotacoes is None:
            return True
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM anotacoes a "
                "JOIN materias m ON m.id_materias = a.id_materias "
                "WHERE a.id_anotacoes = %s AND a.id_materias = %s "
                "AND m.id_usuarios = %s",
                (id_anotacoes, id_materias, id_usuario),
            )
            return cursor.fetchone() is not None

    @staticmethod
    def criar(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "INSERT INTO pomodoro "
                "(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes) "
                "SELECT %s, %s, %s, %s, %s, m.id_materias, %s FROM materias m "
                "WHERE m.id_materias = %s AND m.id_usuarios = %s "
                "AND (%s IS NULL OR EXISTS (SELECT 1 FROM anotacoes a "
                "WHERE a.id_anotacoes = %s AND a.id_materias = m.id_materias)) "
                "RETURNING *",
                (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida,
                 id_anotacoes, id_materias, id_usuario, id_anotacoes, id_anotacoes),
            )
            return cursor.fetchone()

    @staticmethod
    def atualizar(id_pomodoro, inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "UPDATE pomodoro p "
                "SET inicio = %s, duracao_foco_min = %s, duracao_pausa_min = %s, "
                "tipo = %s, concluida = %s, id_materias = %s, id_anotacoes = %s "
                "WHERE p.id_pomodoro = %s "
                "AND EXISTS (SELECT 1 FROM materias origem "
                "WHERE origem.id_materias = p.id_materias AND origem.id_usuarios = %s) "
                "AND EXISTS (SELECT 1 FROM materias destino "
                "WHERE destino.id_materias = %s AND destino.id_usuarios = %s) "
                "AND (%s IS NULL OR EXISTS (SELECT 1 FROM anotacoes a "
                "WHERE a.id_anotacoes = %s AND a.id_materias = %s)) "
                "RETURNING p.*",
                (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida,
                 id_materias, id_anotacoes, id_pomodoro, id_usuario,
                 id_materias, id_usuario, id_anotacoes, id_anotacoes, id_materias),
            )
            return cursor.fetchone()

    @staticmethod
    def deletar(id_pomodoro, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "DELETE FROM pomodoro p WHERE p.id_pomodoro = %s "
                "AND EXISTS (SELECT 1 FROM materias m "
                "WHERE m.id_materias = p.id_materias AND m.id_usuarios = %s) "
                "RETURNING p.id_pomodoro",
                (id_pomodoro, id_usuario),
            )
            return cursor.fetchone() is not None