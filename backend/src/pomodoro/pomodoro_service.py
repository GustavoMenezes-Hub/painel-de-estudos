from src.api_errors import ApiError
from src.pomodoro.pomodoro_repository import PomodoroRepository

class PomodoroService:

    @staticmethod
    def listar_pomodoros(id_materias):
        return PomodoroRepository.listar(id_materias)

    @staticmethod
    def buscar_pomodoro(id_pomodoro):
        pomodoro = PomodoroRepository.buscar_por_id(id_pomodoro)
        if not pomodoro:
            raise ApiError("Registro de Pomodoro não encontrado.", 404)
        return pomodoro

    @staticmethod
    def criar_pomodoro(dados):
        inicio = dados.get("inicio")
        duracao_foco_min = dados.get("duracao_foco_min")
        duracao_pausa_min = dados.get("duracao_pausa_min")
        tipo = dados.get("tipo")
        concluida = dados.get("concluida", False)
        id_materias = dados.get("id_materias")
        id_anotacoes = dados.get("id_anotacoes")

        if not inicio:
            raise ApiError("O campo 'inicio' é obrigatório.", 400)
        
        if duracao_foco_min is None or duracao_foco_min <= 0:
            raise ApiError("O campo 'duracao_foco_min' deve ser maior que 0.", 400)

        if duracao_pausa_min is None or duracao_pausa_min < 0:
            raise ApiError("O campo 'duracao_pausa_min' não pode ser negativo.", 400)

        if not id_materias:
            raise ApiError("O campo 'id_materias' é obrigatório.", 400)

        # Valida se a matéria existe
        if not PomodoroRepository.verificar_materia_existe(id_materias):
            raise ApiError("Matéria informada não foi encontrada.", 404)

        # Valida se a anotação existe (caso tenha sido informada)
        if id_anotacoes and not PomodoroRepository.verificar_anotacao_existe(id_anotacoes):
            raise ApiError("Anotação informada não foi encontrada.", 404)

        return PomodoroRepository.criar(inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes)

    @staticmethod
    def atualizar_pomodoro(id_pomodoro, dados):
        atual = PomodoroService.buscar_pomodoro(id_pomodoro)

        inicio = dados.get("inicio", atual["inicio"])
        duracao_foco_min = dados.get("duracao_foco_min", atual["duracao_foco_min"])
        duracao_pausa_min = dados.get("duracao_pausa_min", atual["duracao_pausa_min"])
        tipo = dados.get("tipo", atual["tipo"])
        concluida = dados.get("concluida", atual["concluida"])
        id_materias = dados.get("id_materias", atual["id_materias"])
        id_anotacoes = dados.get("id_anotacoes", atual["id_anotacoes"])

        if duracao_foco_min <= 0:
            raise ApiError("O campo 'duracao_foco_min' deve ser maior que 0.", 400)

        if duracao_pausa_min < 0:
            raise ApiError("O campo 'duracao_pausa_min' não pode ser negativo.", 400)

        if id_materias != atual["id_materias"]:
            if not PomodoroRepository.verificar_materia_existe(id_materias):
                raise ApiError("Matéria informada não foi encontrada.", 404)

        if id_anotacoes != atual["id_anotacoes"] and id_anotacoes is not None:
            if not PomodoroRepository.verificar_anotacao_existe(id_anotacoes):
                raise ApiError("Anotação informada não foi encontrada.", 404)

        return PomodoroRepository.atualizar(id_pomodoro, inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes)

    @staticmethod
    def deletar_pomodoro(id_pomodoro):
        PomodoroService.buscar_pomodoro(id_pomodoro)
        PomodoroRepository.deletar(id_pomodoro)