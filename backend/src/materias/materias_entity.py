class Materia:
    def __init__(self, id_materias, nome, descricao, id_usuarios, data_criacao=None):
        self.id_materias = id_materias
        self.nome = nome
        self.descricao = descricao
        self.id_usuarios = id_usuarios
        self.data_criacao = data_criacao

    @classmethod
    def from_row(cls, linha):
        return cls(
            id_materias=linha["id_materias"],
            nome=linha["nome"],
            descricao=linha["descricao"],
            id_usuarios=linha["id_usuarios"],
            data_criacao=linha["data_criacao"],
        )

    def to_dict(self):
        return {
            "id_materias": self.id_materias,
            "nome": self.nome,
            "descricao": self.descricao,
            "id_usuarios": self.id_usuarios,
            "data_criacao": self.data_criacao,
        }