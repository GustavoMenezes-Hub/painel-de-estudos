from src.api_errors import ApiError
from src.anotacoes.anotacoes_repository import AnotacoesRepository

class AnotacoesService:

    @staticmethod
    def listar_anotacoes(id_materias):
        return AnotacoesRepository.listar(id_materias)

    @staticmethod
    def buscar_anotacao(id_anotacoes):
        anotacao = AnotacoesRepository.buscar_por_id(id_anotacoes)
        if not anotacao:
            raise ApiError("Anotação não encontrada.", 404)
        return anotacao

    @staticmethod
    def criar_anotacao(dados):
        texto = dados.get("texto")
        id_materias = dados.get("id_materias")
        situacao = dados.get("situacao", "pendente_revisao")

        if not texto or not texto.strip():
            raise ApiError("O campo 'texto' é obrigatório.", 400)
        
        if not id_materias:
            raise ApiError("O campo 'id_materias' é obrigatório.", 400)

        # Valida se a matéria existe
        if not AnotacoesRepository.verificar_materia_existe(id_materias):
            raise ApiError("Matéria informada não foi encontrada.", 404)

        return AnotacoesRepository.criar(texto.strip(), situacao, id_materias)

    @staticmethod
    def atualizar_anotacao(id_anotacoes, dados):
        anotacao_atual = AnotacoesService.buscar_anotacao(id_anotacoes)

        texto = dados.get("texto")
        situacao = dados.get("situacao")
        id_materias = dados.get("id_materias")

        novo_texto = texto.strip() if texto is not None else anotacao_atual["texto"]
        nova_situacao = situacao if situacao is not None else anotacao_atual["situacao"]
        novo_id_materias = id_materias if id_materias is not None else anotacao_atual["id_materias"]

        if novo_id_materias != anotacao_atual["id_materias"]:
            if not AnotacoesRepository.verificar_materia_existe(novo_id_materias):
                raise ApiError("Matéria informada não foi encontrada.", 404)

        return AnotacoesRepository.atualizar(id_anotacoes, novo_texto, nova_situacao, novo_id_materias)

    @staticmethod
    def deletar_anotacao(id_anotacoes):
        # Garante que existe antes de deletar
        AnotacoesService.buscar_anotacao(id_anotacoes)
        AnotacoesRepository.deletar(id_anotacoes)