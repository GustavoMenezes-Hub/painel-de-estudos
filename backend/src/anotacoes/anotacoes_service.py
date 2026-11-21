from src.api_errors import ApiError
from src.validacao import id_filtro, id_postgres, validar_texto_postgres
from src.anotacoes.anotacoes_repository import AnotacoesRepository

class AnotacoesService:

    @staticmethod
    def _id_materia(valor):
        if not id_postgres(valor):
            raise ApiError("id_materias deve ser inteiro positivo.", 400)
        return valor

    @staticmethod
    def _situacao(valor):
        if valor not in ("pendente_revisao", "iniciar_estudo", "estudada"):
            raise ApiError("Situação inválida para anotação.", 400)
        return valor

    @staticmethod
    def _texto(valor):
        validar_texto_postgres(valor, "texto", maximo=10_000)
        if not isinstance(valor, str) or not valor.strip():
            raise ApiError("O campo 'texto' é obrigatório.", 400)
        return valor.strip()

    @staticmethod
    def listar_anotacoes(id_materias, id_usuario):
        id_materias = id_filtro(id_materias)
        return AnotacoesRepository.listar(id_usuario, id_materias)

    @staticmethod
    def buscar_anotacao(id_anotacoes, id_usuario):
        anotacao = AnotacoesRepository.buscar_por_id(id_anotacoes, id_usuario)
        if anotacao is None:
            raise ApiError("Anotação não encontrada para este usuário.", 404)
        return anotacao

    @staticmethod
    def criar_anotacao(dados, id_usuario):
        if not isinstance(dados, dict):
            raise ApiError("Envie um objeto JSON.", 400)
        texto = AnotacoesService._texto(dados.get("texto"))
        id_materias = AnotacoesService._id_materia(dados.get("id_materias"))
        situacao = AnotacoesService._situacao(dados.get("situacao", "pendente_revisao"))
        if not AnotacoesRepository.verificar_materia_existe(id_materias, id_usuario):
            raise ApiError("Matéria não encontrada para este usuário.", 404)
        nova = AnotacoesRepository.criar(texto, situacao, id_materias, id_usuario)
        if nova is None:
            raise ApiError("Matéria não encontrada para este usuário.", 404)
        return nova

    @staticmethod
    def atualizar_anotacao(id_anotacoes, dados, id_usuario):
        if not isinstance(dados, dict):
            raise ApiError("Envie um objeto JSON.", 400)
        validadores = {
            "texto": AnotacoesService._texto,
            "situacao": AnotacoesService._situacao,
            "id_materias": AnotacoesService._id_materia,
        }
        campos = {campo: validar(dados[campo]) for campo, validar in validadores.items() if campo in dados}
        if not campos:
            raise ApiError("Informe texto, situacao ou id_materias para atualizar.", 400)
        atualizada = AnotacoesRepository.atualizar(id_anotacoes, campos, id_usuario)
        if atualizada is None:
            raise ApiError("Anotação não encontrada para este usuário.", 404)
        return atualizada

    @staticmethod
    def deletar_anotacao(id_anotacoes, id_usuario):
        if not AnotacoesRepository.deletar(id_anotacoes, id_usuario):
            raise ApiError("Anotação não encontrada para este usuário.", 404)
