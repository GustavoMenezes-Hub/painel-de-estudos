import re
from datetime import datetime, timezone
from src.api_errors import ApiError
from src.validacao import MAX_INTEIRO_POSTGRES, id_filtro, id_postgres, validar_texto_postgres
from src.pomodoro.pomodoro_repository import PomodoroRepository

HORA_COM_FUSO = re.compile(
    r"[T ]\d{2}(?::?\d{2}(?::?\d{2})?)?(?:[.,]\d+)?"
    r"(?:Z|[+-](?:[01]\d|2[0-3])(?::?[0-5]\d)?)\Z", re.ASCII
)

class PomodoroService:

    @staticmethod
    def _id(valor, campo, opcional=False):
        if opcional and valor is None:
            return None
        if not id_postgres(valor):
            raise ApiError(f"{campo} deve ser inteiro positivo.", 400)
        return valor

    @staticmethod
    def _duracao(valor, campo, minimo):
        if type(valor) is not int or not minimo <= valor <= MAX_INTEIRO_POSTGRES:
            raise ApiError(f"{campo} deve ser inteiro entre {minimo} e {MAX_INTEIRO_POSTGRES}.", 400)
        return valor

    @staticmethod
    def _inicio(valor):
        mensagem = "O campo 'inicio' deve ser uma data e hora ISO 8601 com fuso explícito (Z ou deslocamento)."
        if not isinstance(valor, str) or not HORA_COM_FUSO.search(valor):
            raise ApiError(mensagem)
        try:
            return datetime.fromisoformat(valor).astimezone(timezone.utc)
        except (ValueError, OverflowError):
            raise ApiError(mensagem) from None

    @staticmethod
    def _validar_tipo(valor):
        if valor is not None and (not isinstance(valor, str) or len(valor) > 50):
            raise ApiError("O campo 'tipo' deve ser texto de até 50 caracteres.", 400)
        validar_texto_postgres(valor, "tipo")
        return valor

    @staticmethod
    def _validar_concluida(valor):
        if type(valor) is not bool:
            raise ApiError("O campo 'concluida' deve ser booleano.", 400)
        return valor

    @staticmethod
    def listar_pomodoros(id_materias, id_usuario):
        id_materias = id_filtro(id_materias)
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
        novo = PomodoroRepository.criar(inicio, duracao_foco_min, duracao_pausa_min,
                                        tipo, concluida, id_materias, id_anotacoes, id_usuario)
        if novo is None:
            raise ApiError("Matéria ou anotação não encontrada para este usuário.", 404)
        return novo

    @staticmethod
    def atualizar_pomodoro(id_pomodoro, dados, id_usuario):
        if not isinstance(dados, dict):
            raise ApiError("Envie um objeto JSON.", 400)
        validadores = {
            "inicio": PomodoroService._inicio,
            "duracao_foco_min": lambda valor: PomodoroService._duracao(valor, "duracao_foco_min", 1),
            "duracao_pausa_min": lambda valor: PomodoroService._duracao(valor, "duracao_pausa_min", 0),
            "tipo": PomodoroService._validar_tipo,
            "concluida": PomodoroService._validar_concluida,
            "id_materias": lambda valor: PomodoroService._id(valor, "id_materias"),
            "id_anotacoes": lambda valor: PomodoroService._id(valor, "id_anotacoes", opcional=True),
        }
        campos = {campo: validar(dados[campo]) for campo, validar in validadores.items() if campo in dados}
        if not campos:
            raise ApiError("Informe pelo menos um campo de Pomodoro para atualizar.", 400)
        atualizado = PomodoroRepository.atualizar(id_pomodoro, campos, id_usuario)
        if atualizado is None:
            raise ApiError("Registro de Pomodoro não encontrado para este usuário.", 404)
        return atualizado

    @staticmethod
    def deletar_pomodoro(id_pomodoro, id_usuario):
        if not PomodoroRepository.deletar(id_pomodoro, id_usuario):
            raise ApiError("Registro de Pomodoro não encontrado para este usuário.", 404)
