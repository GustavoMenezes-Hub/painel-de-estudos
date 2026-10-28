from datetime import datetime
from src.api_errors import ApiError
from src.pomodoro.pomodoro_repository import PomodoroRepository

class PomodoroService:

    @staticmethod
    def _id(valor, campo, opcional=False):
        if opcional and valor is None:
            return None
        if type(valor) is not int or valor <= 0:
            raise ApiError(f"{campo} deve ser inteiro positivo.", 400)
        return valor

    @staticmethod
    def _duracao(valor, campo, minimo):
        if type(valor) is not int or valor < minimo:
            raise ApiError(f"{campo} deve ser inteiro maior ou igual a {minimo}.", 400)
        return valor

    @staticmethod
    def _inicio(valor):
        if not isinstance(valor, str):
            raise ApiError("O campo 'inicio' deve ser data e hora ISO 8601.", 400)
        try:
            inicio = datetime.fromisoformat(valor)
        except ValueError:
            raise ApiError("O campo 'inicio' deve ser data e hora ISO 8601.", 400)
        return valor

    @staticmethod
    def _validar_tipo(valor):
        if valor is not None and (not isinstance(valor, str) or len(valor) > 50):
            raise ApiError("O campo 'tipo' deve ser texto de até 50 caracteres.", 400)
        return valor

    @staticmethod
    def _validar_concluida(valor):
        if type(valor) is not bool:
            raise ApiError("O campo 'concluida' deve ser booleano.", 400)
        return valor

    @staticmethod
    def _validar_relacoes(id_materias, id_anotacoes, id_usuario):
        if not PomodoroRepository.verificar_materia_existe(id_materias, id_usuario):
            raise ApiError("Matéria não encontrada para este usuário.", 404)
        if not PomodoroRepository.verificar_anotacao_existe(id_anotacoes, id_materias, id_usuario):
            raise ApiError("Anotação não encontrada nessa matéria para este usuário.", 404)

    @staticmethod
    def listar_pomodoros(id_materias, id_usuario):
        if id_materias is not None:
            if not id_materias.isdecimal() or int(id_materias) <= 0:
                raise ApiError("id_materias deve ser inteiro positivo.", 400)
            id_materias = int(id_materias)
        return PomodoroRepository.listar(id_usuario, id_materias)

    @staticmethod
    def buscar_pomodoro(id_pomodoro, id_usuario):
        pomodoro = PomodoroRepository.buscar_por_id(id_pomodoro, id_usuario)
        if pomodoro is None:
            raise ApiError("Registro de Pomodoro não encontrado para este usuário.", 404)
        return pomodoro

    @staticmethod
    def criar_pomodoro(dados, id_usuario):
        if not isinstance(dados, dict):
            raise ApiError("Envie um objeto JSON.", 400)
        inicio = PomodoroService._inicio(dados.get("inicio"))
        duracao_foco_min = PomodoroService._duracao(dados.get("duracao_foco_min"), "duracao_foco_min", 1)
        duracao_pausa_min = PomodoroService._duracao(dados.get("duracao_pausa_min"), "duracao_pausa_min", 0)
        tipo = PomodoroService._validar_tipo(dados.get("tipo"))
        concluida = PomodoroService._validar_concluida(dados.get("concluida", False))
        id_materias = PomodoroService._id(dados.get("id_materias"), "id_materias")
        id_anotacoes = PomodoroService._id(dados.get("id_anotacoes"), "id_anotacoes", opcional=True)
        PomodoroService._validar_relacoes(id_materias, id_anotacoes, id_usuario)
        novo = PomodoroRepository.criar(inicio, duracao_foco_min, duracao_pausa_min,
                                        tipo, concluida, id_materias, id_anotacoes, id_usuario)
        if novo is None:
            raise ApiError("Matéria ou anotação não encontrada para este usuário.", 404)
        return novo

    @staticmethod
    def atualizar_pomodoro(id_pomodoro, dados, id_usuario):
        atual = PomodoroService.buscar_pomodoro(id_pomodoro, id_usuario)
        if not isinstance(dados, dict) or not dados:
            raise ApiError("Informe campos para atualizar.", 400)
        inicio = (PomodoroService._inicio(dados["inicio"])
                  if "inicio" in dados else atual["inicio"])
        duracao_foco_min = PomodoroService._duracao(
            dados.get("duracao_foco_min", atual["duracao_foco_min"]), "duracao_foco_min", 1)
        duracao_pausa_min = PomodoroService._duracao(
            dados.get("duracao_pausa_min", atual["duracao_pausa_min"]), "duracao_pausa_min", 0)
        tipo = PomodoroService._validar_tipo(dados.get("tipo", atual["tipo"]))
        concluida = PomodoroService._validar_concluida(dados.get("concluida", atual["concluida"]))
        id_materias = PomodoroService._id(dados.get("id_materias", atual["id_materias"]), "id_materias")
        id_anotacoes = PomodoroService._id(dados.get("id_anotacoes", atual["id_anotacoes"]),
                                           "id_anotacoes", opcional=True)
        PomodoroService._validar_relacoes(id_materias, id_anotacoes, id_usuario)
        atualizado = PomodoroRepository.atualizar(
            id_pomodoro, inicio, duracao_foco_min, duracao_pausa_min,
            tipo, concluida, id_materias, id_anotacoes, id_usuario)
        if atualizado is None:
            raise ApiError("Registro de Pomodoro não encontrado para este usuário.", 404)
        return atualizado

    @staticmethod
    def deletar_pomodoro(id_pomodoro, id_usuario):
        if not PomodoroRepository.deletar(id_pomodoro, id_usuario):
            raise ApiError("Registro de Pomodoro não encontrado para este usuário.", 404)