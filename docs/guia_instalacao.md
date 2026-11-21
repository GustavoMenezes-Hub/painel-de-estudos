# Executar o backend do Painel de Estudos

## Ambiente local

Use PostgreSQL 15 ou superior e Python com suporte às versões de [requirements.txt](../backend/requirements.txt). O ambiente da entrega foi testado com Python 3.14 e PostgreSQL 18. Execute os comandos a partir da raiz de `painel-de-estudos`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

Em uma instalação nova, crie o banco `painel_estudos` e copie `backend/.env.example` para `.env` na raiz. Preencha `DATABASE_URL` com a conexão PostgreSQL e `SECRET_KEY` com uma chave privada aleatória. O comando abaixo gera uma chave. Guarde a mesma chave entre reinícios para manter a validade dos tokens.

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Banco e servidor

```powershell
cd backend
python migrate.py
python -m flask --app src.app run --host 127.0.0.1 --port 3000
```

O migrador registra os arquivos aplicados em `schema_migrations` e executa as operações pendentes em uma transação. Para atualizar uma instalação antiga que tenha usuários sem hash de senha, execute `python migrate.py --recuperar-contas`. O terminal solicita uma nova senha para cada conta pendente.

### Conta fictícia para avaliação

Após as migrations, execute `python seed.py` dentro de `backend`. A seed cria um usuário comum para o professor acessar a API com `POST /api/login`.

| Nome | E-mail | Senha de demonstração |
| --- | --- | --- |
| `usuarioteste` | `test123@gmail.com` | `Test1234!` |

A conta recebe cinco matérias, quatro entregas, três anotações e duas sessões Pomodoro. Se o e-mail já existir, a seed preserva a conta, a senha e os registros associados. As credenciais da tabela são públicas e destinadas à demonstração.

## Contrato da API

O [Swagger](http://127.0.0.1:3000/apidocs/) e a [especificação JSON](http://127.0.0.1:3000/apispec_1.json) apresentam todos os métodos, campos de entrada e saída, filtros e códigos de resposta. Os corpos de requisição usam `application/json`. Erros da API usam o objeto `{"erro": "mensagem"}`.

| Recurso | Coleção | Item |
| --- | --- | --- |
| Usuários | `GET`, `POST /api/usuarios` | `GET`, `PUT`, `PATCH`, `DELETE /api/usuarios/{id_usuario}` |
| Matérias | `GET`, `POST /api/materias` | `GET`, `PUT`, `DELETE /api/materias/{id_materias}` |
| Entregas | `GET`, `POST /api/entregas` | `GET`, `PUT`, `PATCH`, `DELETE /api/entregas/{id_entrega}` |
| Anotações | `GET`, `POST /api/anotacoes` | `GET`, `PUT`, `PATCH`, `DELETE /api/anotacoes/{id_anotacoes}` |
| Pomodoro | `GET`, `POST /api/pomodoro` | `GET`, `PUT`, `PATCH`, `DELETE /api/pomodoro/{id_pomodoro}` |

1. Cadastre uma conta em `POST /api/usuarios` com `nome`, `email` e `senha` de 8 a 128 caracteres. A resposta é `201`.
2. Envie `email` e `senha` a `POST /api/login`. A resposta `200` contém `access_token`, `token_type`, `expires_in` em segundos e o resumo do usuário.
3. Envie `Authorization: Bearer <access_token>` nas chamadas protegidas. `GET /api/usuarios/me` devolve o perfil. `GET /api/usuarios` lista o resumo da própria conta. O token dura 24 horas e a troca de senha exige novo login.
4. Crie uma matéria com `POST /api/materias` e um corpo como `{"nome":"Banco de Dados"}`. Use o `id_materias` retornado para criar os registros dependentes.

`GET /api/materias/{id_materias}/entregas` lista as entregas da matéria. `GET /api/notas` também lista anotações. As coleções de anotações e Pomodoro aceitam o filtro `?id_materias=1`.

O `PUT` de matérias exige `nome` e limpa a descrição quando omitida. Nos demais recursos, `PUT` e `PATCH` atualizam os campos enviados. Datas de vencimento usam `AAAA-MM-DD`.

### Tamanho do JSON e dos campos

| Entrada | Limite inclusivo | Comportamento |
| --- | --- | --- |
| Corpo JSON completo | 1 MB (1.048.576 bytes) | O Flask conta os bytes transmitidos, inclusive espaços e sintaxe JSON. Acima do limite, retorna `413` com `{"erro":"O corpo da requisição deve ter até 1 MB (1.048.576 bytes)."}`. |
| Texto de anotação | 10.000 caracteres | Obrigatório na criação. O serviço conta os caracteres antes de remover espaços das bordas. |
| Descrição de matéria | 2.000 caracteres | Opcional. Omissão, `null` ou texto em branco dentro do limite resultam em descrição nula. |
| Senha | 8 a 128 caracteres ao definir ou trocar | Espaços fazem parte da senha. O login também rejeita mais de 128 caracteres antes de consultar a conta. Uma tentativa com senha não vazia e incorreta dentro do máximo continua recebendo `401`. |

O excesso em um campo de um JSON dentro de 1 MB retorna `400` com a chave `erro`. O serviço recusa o valor inteiro. Por exemplo, uma anotação de 10.001 caracteres recebe `{"erro":"O campo 'texto' deve ter até 10000 caracteres."}`. Os limites dos campos contam caracteres da string decodificada. Um caractere como `á` conta uma vez, embora possa ocupar mais de um byte no JSON. A API desta versão recebe dados em JSON.

### Início de uma sessão Pomodoro

Em `POST /api/pomodoro`, envie `inicio` em ISO 8601 com fuso explícito. `2026-11-21T12:00:00-03:00` e `2026-11-21T15:00:00Z` representam o mesmo instante. O serviço converte para UTC antes da escrita em `TIMESTAMPTZ`. Na leitura, o deslocamento exibido pode acompanhar o fuso da conexão PostgreSQL.

Uma data sem fuso, como `2026-11-21T12:00:00`, ou uma data impossível, como `2026-02-30T12:00:00Z`, recebe `400` com a chave `erro`. A mesma regra vale em `PUT` e `PATCH` quando `inicio` é enviado. Omitir o campo na alteração preserva o instante anterior.

## Integridade e exclusão

Cada matéria pertence a um usuário e reúne suas entregas, anotações e sessões. A sessão pode referenciar uma anotação da mesma matéria. O banco exige um hash de senha, garante a unicidade de e-mail sem distinção entre maiúsculas e minúsculas e valida situações e durações.

Excluir uma matéria exclui seus registros dependentes. Excluir uma anotação mantém as sessões e limpa a referência à anotação. Uma conta com matérias recebe `409` ao tentar a exclusão. Mover uma anotação vinculada para outra matéria também retorna `409`.

## Testes

Dentro de `backend`, com o ambiente virtual ativo, execute:

```powershell
python -B -m unittest discover -s tests -v
```

O comando descobre os dois módulos em `backend/tests`. O arquivo `test_validacao.py` verifica as regras de identificadores em memória. O arquivo `test_integracao.py` testa a API e o PostgreSQL, incluindo duas execuções da seed seguidas de login com a conta fictícia e conferência das quantidades de registros.

A suíte também compara o instante do Pomodoro em conexões configuradas com `UTC`, `America/Fortaleza` e `Asia/Kathmandu`. Exercita os limites por campo, o corpo JSON um byte abaixo, exatamente no limite e um byte acima, e as respostas JSON `400` e `413`. O teste do contrato compara as 33 operações nos seis grupos do Swagger às rotas registradas no Flask. A opção `-B` evita gravar bytecode Python durante a execução.

A suíte de integração usa a conexão configurada para criar um banco exclusivo com nome aleatório no mesmo servidor e o remove ao terminar. O papel PostgreSQL usado nos testes precisa da permissão `CREATEDB`. A suíte cobre escrita real, concorrência, acesso entre contas, autenticação, migrations e inicialização HTTP. A aplicação em execução requer somente as permissões sobre seus dados e sequências.
