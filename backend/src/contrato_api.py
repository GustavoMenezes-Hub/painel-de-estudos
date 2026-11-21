"Contrato Swagger servido pelo Flasgger em /apispec_1.json."
INTEIRO = {"type": "integer", "format": "int32", "minimum": 1, "maximum": 2147483647}
TEXTO = {"type": "string", "minLength": 1}
NOME = {**TEXTO, "maxLength": 100}
DATA_HORA = {"type": "string", "format": "date-time"}
EMAIL = {**NOME, "format": "email"}
SENHA = {"type": "string", "format": "password", "minLength": 8}

def objeto(propriedades, obrigatorios=()):
    schema = {"type": "object", "properties": propriedades}
    if obrigatorios:
        schema["required"] = list(obrigatorios)
    return schema

def ref(nome):
    return {"$ref": "#/definitions/" + nome}

def lista(nome):
    return {"type": "array", "items": ref(nome)}

def especificacao():
    usuario = {"nome": NOME, "email": EMAIL, "senha": SENHA}
    materia = {"nome": NOME, "descricao": {"type": "string", "x-nullable": True}}
    entrega = {"titulo": NOME, "data_vencimento": {"type": "string", "format": "date"},
               "situacao": {"type": "string", "enum": ["pendente", "realizado"], "default": "pendente"},
               "id_materias": INTEIRO}
    anotacao = {"texto": TEXTO, "situacao": {"type": "string", "default": "pendente_revisao",
                "enum": ["pendente_revisao", "iniciar_estudo", "estudada"]}, "id_materias": INTEIRO}
    pomodoro = {"inicio": DATA_HORA, "duracao_foco_min": INTEIRO,
                "duracao_pausa_min": {**INTEIRO, "minimum": 0},
                "tipo": {"type": "string", "maxLength": 50, "x-nullable": True},
                "concluida": {"type": "boolean", "default": False}, "id_materias": INTEIRO,
                "id_anotacoes": {**INTEIRO, "x-nullable": True}}
    perfil = {"id_usuarios": INTEIRO, "nome": NOME, "email": EMAIL}
    definicoes = {
        "Erro": objeto({"erro": TEXTO}, ["erro"]),
        "Mensagem": objeto({"mensagem": TEXTO}, ["mensagem"]),
        "ResumoUsuario": objeto({"id_usuarios": INTEIRO, "nome": NOME}),
        "Login": objeto({"email": EMAIL, "senha": {"type": "string", "format": "password"}}, ["email", "senha"]),
        "Sessao": objeto({"access_token": TEXTO, "token_type": {"type": "string", "enum": ["Bearer"]},
                         "expires_in": {"type": "integer", "example": 86400}, "usuario": objeto(perfil)}),
    }
    caminhos = {}
    erros = {400: "Parâmetro ou JSON inválido.", 401: "Autenticação inválida ou expirada.",
             403: "O perfil pertence a outro usuário.", 404: "Recurso indisponível para o usuário.",
             409: "Duplicidade ou conflito entre registros.", 503: "PostgreSQL indisponível."}

    def operacao(rota, metodo, resumo, tag, resposta, status=200, *, corpo=None, publica=False,
                 falhas=(), filtro=False):
        parametros = []
        for segmento in rota.split("/"):
            if segmento.startswith("{"):
                parametros.append({"name": segmento[1:-1], "in": "path", "required": True, **INTEIRO})
        if filtro:
            parametros.append({"name": "id_materias", "in": "query", **INTEIRO})
        if corpo:
            parametros.append({"name": "dados", "in": "body", "required": True, "schema": ref(corpo)})
        sucesso = {"description": resumo}
        if resposta is not None:
            sucesso["schema"] = resposta
        respostas = {str(status): sucesso}
        for codigo in sorted(set(falhas) | {503} | (set() if publica else {401})):
            respostas[str(codigo)] = {"description": erros[codigo], "schema": ref("Erro")}
        caminhos.setdefault(rota, {})[metodo] = {
            "tags": [tag], "summary": resumo, "security": [] if publica else [{"Bearer": []}],
            "parameters": parametros, "responses": respostas,
        }

    recursos = [
        ("usuarios", "Usuario", "id_usuario", usuario, list(usuario), {**perfil, "data_criacao": DATA_HORA}),
        ("materias", "Materia", "id_materias", materia, ["nome"],
         {**materia, "id_materias": INTEIRO, "id_usuarios": INTEIRO, "data_criacao": DATA_HORA}),
        ("entregas", "Entrega", "id_entrega", entrega, ["titulo", "data_vencimento", "id_materias"],
         {**entrega, "id_entregas": INTEIRO, "data_criacao": DATA_HORA}),
        ("anotacoes", "Anotacao", "id_anotacoes", anotacao, ["texto", "id_materias"],
         {**anotacao, "id_anotacoes": INTEIRO, "data_criacao": DATA_HORA}),
        ("pomodoro", "Pomodoro", "id_pomodoro", pomodoro,
         ["inicio", "duracao_foco_min", "duracao_pausa_min", "id_materias"], {**pomodoro, "id_pomodoro": INTEIRO}),
    ]
    apresentacao = {
        "usuarios": {
            "grupo": "Usuários",
            "listar": "Lista o identificador e o nome da própria conta.",
            "criar": "Cria uma conta de estudante.",
            "buscar": "Busca o perfil da própria conta pelo identificador.",
            "atualizar": "Atualiza o nome, o e-mail ou a senha da própria conta.",
            "excluir": "Exclui a própria conta quando ela já não tem matérias cadastradas.",
        },
        "materias": {
            "grupo": "Matérias",
            "listar": "Lista as matérias cadastradas pelo usuário.",
            "criar": "Cadastra uma nova matéria.",
            "buscar": "Busca uma matéria pelo identificador.",
            "atualizar": "Atualiza uma matéria. A descrição é apagada se for omitida.",
            "excluir": "Exclui uma matéria e suas entregas, anotações e sessões Pomodoro.",
        },
        "entregas": {
            "grupo": "Entregas",
            "listar": "Lista as entregas de todas as matérias do usuário.",
            "criar": "Cadastra uma entrega para uma matéria.",
            "buscar": "Busca uma entrega pelo identificador.",
            "atualizar": "Atualiza o título, o vencimento, a situação ou a matéria de uma entrega.",
            "excluir": "Exclui uma entrega.",
        },
        "anotacoes": {
            "grupo": "Anotações",
            "listar": "Lista as anotações do usuário, com opção de filtrar por matéria.",
            "criar": "Salva uma nova anotação em uma matéria.",
            "buscar": "Busca uma anotação pelo identificador.",
            "atualizar": "Atualiza o texto, a situação de estudo ou a matéria de uma anotação.",
            "excluir": "Exclui uma anotação e preserva as sessões Pomodoro que a usaram.",
        },
        "pomodoro": {
            "grupo": "Pomodoro",
            "listar": "Lista as sessões Pomodoro do usuário, da mais recente para a mais antiga.",
            "criar": "Registra uma sessão Pomodoro para uma matéria.",
            "buscar": "Busca uma sessão Pomodoro pelo identificador.",
            "atualizar": "Atualiza os dados da sessão Pomodoro ou marca sua conclusão.",
            "excluir": "Exclui uma sessão Pomodoro.",
        },
    }
    for recurso, nome, chave, campos, obrigatorios, saida in recursos:
        texto = apresentacao[recurso]
        grupo = texto["grupo"]
        colecao = "/api/" + recurso
        item = colecao + "/{" + chave + "}"
        definicoes[nome] = objeto(saida)
        definicoes[nome + "Cadastro"] = objeto(campos, obrigatorios)
        definicoes[nome + "Alteracao"] = objeto(campos, ["nome"] if recurso == "materias" else [])
        filtra_materia = recurso in ("anotacoes", "pomodoro")
        operacao(colecao, "get", texto["listar"], grupo, lista("ResumoUsuario" if recurso == "usuarios" else nome),
                 filtro=filtra_materia, falhas=(400,) if filtra_materia else ())
        operacao(colecao, "post", texto["criar"], grupo, ref(nome), 201, corpo=nome + "Cadastro",
                 publica=recurso == "usuarios", falhas=(400, 409) if recurso == "usuarios" else (400, 404, 409))
        falhas = (400, 403, 404) if recurso == "usuarios" else (400, 404)
        operacao(item, "get", texto["buscar"], grupo, ref(nome), falhas=falhas)
        for metodo in (["put"] if recurso == "materias" else ["put", "patch"]):
            operacao(item, metodo, texto["atualizar"], grupo, ref(nome), corpo=nome + "Alteracao", falhas=(*falhas, 409))
        mensagem = recurso in ("pomodoro", "anotacoes")
        operacao(item, "delete", texto["excluir"], grupo, ref("Mensagem") if mensagem else None,
                 200 if mensagem else 204, falhas=(*falhas, 409))
    operacao("/api/login", "post", "Confere o e-mail e a senha e fornece um token de acesso.", "Autenticação", ref("Sessao"),
             corpo="Login", publica=True, falhas=(400, 401))
    operacao("/api/usuarios/me", "get", "Mostra o perfil do usuário que está usando a API.", "Usuários", ref("Usuario"))
    operacao("/api/notas", "get", "Lista as anotações do usuário pelo caminho da primeira entrega.", "Anotações",
             lista("Anotacao"), filtro=True, falhas=(400,))
    operacao("/api/materias/{id_materias}/entregas", "get", "Lista as entregas da matéria escolhida.",
             "Entregas", lista("Entrega"), falhas=(400, 404))
    return {
        "swagger": "2.0", "info": {
            "title": "API Painel de Estudos", "version": "1.0.0",
            "description": "O corpo JSON pode ter até 1 MB (1.048.576 bytes). Acima desse tamanho, a API "
                           "responde com 413. A anotação aceita até 10.000 caracteres, a descrição de matéria "
                           "até 2.000 e a senha até 128. Informe o início do Pomodoro com Z ou deslocamento "
                           "de fuso, como 2026-11-21T12:00:00-03:00. Campos fora desses limites ou um "
                           "início inválido recebem 400.",
        },
        "consumes": ["application/json"], "produces": ["application/json"],
        "securityDefinitions": {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization",
                                           "description": "Bearer seguido de um espaço e do access_token."}},
        "definitions": definicoes, "paths": caminhos,
    }
