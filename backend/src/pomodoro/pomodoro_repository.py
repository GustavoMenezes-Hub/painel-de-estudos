from src.api_errors import ApiError
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
    def _bloquear_anotacao(cursor, id_anotacoes, id_materias, id_usuario):
        if id_anotacoes is None:
            return
        # Serializa a vinculação com a mudança de matéria feita pelo CRUD de anotações.
        cursor.execute(
            "SELECT 1 FROM anotacoes a JOIN materias m USING (id_materias) "
            "WHERE a.id_anotacoes = %s AND a.id_materias = %s "
            "AND m.id_usuarios = %s FOR SHARE OF a",
            (id_anotacoes, id_materias, id_usuario),
        )
        if cursor.fetchone() is None:
            raise ApiError("Anotação não encontrada nessa matéria para este usuário.", 404)

    @staticmethod
    def criar(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes, id_usuario):
        with db_cursor() as cursor:
            PomodoroRepository._bloquear_anotacao(cursor, id_anotacoes, id_materias, id_usuario)
            cursor.execute(
                "INSERT INTO pomodoro "
                "(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes) "
                "SELECT %s, %s, %s, %s, %s, m.id_materias, %s FROM materias m "
                "WHERE m.id_materias = %s AND m.id_usuarios = %s RETURNING *",
                (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida,
                 id_anotacoes, id_materias, id_usuario),
            )
            return cursor.fetchone()

    @staticmethod
    def atualizar(id_pomodoro, campos, id_usuario):
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT p.* FROM pomodoro p JOIN materias m USING (id_materias) "
                "WHERE p.id_pomodoro = %s AND m.id_usuarios = %s FOR UPDATE OF p",
                (id_pomodoro, id_usuario),
            )
            atual = cursor.fetchone()
            if atual is None:
                return None
            atual.update(campos)
            PomodoroRepository._bloquear_anotacao(
                cursor, atual["id_anotacoes"], atual["id_materias"], id_usuario
            )
            cursor.execute(
                "UPDATE pomodoro p SET inicio = %s, duracao_foco_min = %s, "
                "duracao_pausa_min = %s, tipo = %s, concluida = %s, "
                "id_materias = m.id_materias, id_anotacoes = %s "
                "FROM materias m WHERE p.id_pomodoro = %s "
                "AND m.id_materias = %s AND m.id_usuarios = %s RETURNING p.*",
                (atual["inicio"], atual["duracao_foco_min"], atual["duracao_pausa_min"],
                 atual["tipo"], atual["concluida"], atual["id_anotacoes"],
                 id_pomodoro, atual["id_materias"], id_usuario),
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