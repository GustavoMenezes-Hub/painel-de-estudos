from src.api_errors import ApiError
from src.anotacoes.anotacoes_repository import AnotacoesRepository

class AnotacoesService:

    @staticmethod
    def _id_materia(valor):
        if type(valor) is not int or valor <= 0:
            raise ApiError("id_materias deve ser inteiro positivo.", 400)
        return valor

    @staticmethod
    def _situacao(valor):
        if valor not in ("pendente_revisao", "iniciar_estudo", "estudada"):
            raise ApiError("Situação inválida para anotação.", 400)
        return valor

    @staticmethod
    def _texto(valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ApiError("O campo 'texto' é obrigatório.", 400)
        return valor.strip()

    @staticmethod
    def listar_anotacoes(id_materias, id_usuario):
        if id_materias is not None:
            if not id_materias.isdecimal() or int(id_materias) <= 0:
                raise ApiError("id_materias deve ser inteiro positivo.", 400)
            id_materias = int(id_materias)
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
        atual = AnotacoesService.buscar_anotacao(id_anotacoes, id_usuario)
        if not isinstance(dados, dict) or not dados:
            raise ApiError("Informe campos para atualizar.", 400)
        texto = AnotacoesService._texto(dados["texto"]) if "texto" in dados else atual["texto"]
        situacao = AnotacoesService._situacao(dados["situacao"]) if "situacao" in dados else atual["situacao"]
        id_materias = (AnotacoesService._id_materia(dados["id_materias"])
                       if "id_materias" in dados else atual["id_materias"])
        if not AnotacoesRepository.verificar_materia_existe(id_materias, id_usuario):
            raise ApiError("Matéria não encontrada para este usuário.", 404)
        if AnotacoesRepository.vinculada_a_pomodoro_de_outra_materia(
            id_anotacoes, id_materias, id_usuario
        ):
            raise ApiError("Não é possível mover uma anotação vinculada a Pomodoro de outra matéria.", 409)
        atualizada = AnotacoesRepository.atualizar(
            id_anotacoes, texto, situacao, id_materias, id_usuario
        )
        if atualizada is None:
            raise ApiError("Anotação não encontrada para este usuário.", 404)
        return atualizada

    @staticmethod
    def deletar_anotacao(id_anotacoes, id_usuario):
        if not AnotacoesRepository.deletar(id_anotacoes, id_usuario):
            raise ApiError("Anotação não encontrada para este usuário.", 404)