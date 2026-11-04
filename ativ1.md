# Atividade 1

## 1. Quais tabelas você definiu inicialmente?

Inicialmente foram definidas três tabelas: `materias`, `entregas` e `notas`.

Ao longo do desenvolvimento o modelo evoluiu, e a tabela `notas` passou a se chamar `anotacoes`. O modelo atual possui **cinco tabelas**:

- `usuarios`
- `materias`
- `entregas`
- `anotacoes`
- `pomodoro`

## 2. Você utilizou migrations? Se sim, quantas migrations? Descreva em uma frase o que cada uma faz.

Sim, **sete migrations**, executadas em ordem pelo script `backend/migrate.py`:

| Migration | O que faz |
|---|---|
| `001_create_usuarios` | Cria a tabela `usuarios`, com nome, e-mail único e data de criação. |
| `002_create_materias` | Cria a tabela `materias`, que armazena as disciplinas e pertence a um usuário por meio da chave estrangeira `id_usuarios`. |
| `003_create_entregas` | Cria a tabela `entregas`, com título, data de vencimento e situação (`pendente` ou `realizado`), vinculada a uma matéria com `ON DELETE CASCADE`. |
| `004_create_anotacoes` | Cria a tabela `anotacoes`, com texto e situação (`pendente_revisao`, `iniciar_estudo` ou `estudada`), vinculada a uma matéria com `ON DELETE CASCADE`. |
| `005_create_pomodoro` | Cria a tabela `pomodoro`, que registra sessões de foco e pausa vinculadas a uma matéria (`ON DELETE CASCADE`) e, opcionalmente, a uma anotação (`ON DELETE SET NULL`). |
| `006_add_senha_hash` | Adiciona a coluna `senha_hash` à tabela `usuarios`, necessária para a autenticação. |
| `007_create_add_imagem_anotacoes` | Adiciona à tabela `anotacoes` as colunas `imagem`, `imagem_tipo` e `imagem_nome`, com uma restrição sobre o tipo de imagem aceito. |

## 3. Qual o caminho do arquivo que gera a seed do seu banco?

`backend/seed.sql`

O arquivo é executado pelo script `backend/seed.py`. Ele limpa as cinco tabelas (`TRUNCATE ... RESTART IDENTITY CASCADE`) e insere dados de exemplo: um usuário, cinco matérias, quatro entregas, três anotações e duas sessões de pomodoro.

## 4. Quais os endpoints que você irá implementar inicialmente? Cada endpoint deve ser um método e um path. Explique em um parágrafo por que você resolveu priorizar a implementação desses endpoints.

**Endpoints priorizados inicialmente:**

```
GET  /api/materias
POST /api/materias
GET  /api/entregas
POST /api/entregas
GET  /api/anotacoes
```

Esses endpoints foram priorizados porque representam as operações primárias da aplicação: são os primeiros dados solicitados assim que o usuário abre o programa, ou seja, as matérias, suas entregas e as anotações associadas. Sem esses endpoints básicos de listagem e criação, nenhuma outra funcionalidade do painel consegue funcionar, já que todas dependem desses recursos existirem primeiro.

**Endpoints implementados atualmente** (todos exigem token `Bearer`, exceto os dois públicos):

| Recurso | Método e path |
|---|---|
| Autenticação | `POST /api/login` (público) |
| Usuários | `POST /api/usuarios` (público), `GET /api/usuarios`, `GET /api/usuarios/me`, `GET /api/usuarios/<id>`, `PUT` e `PATCH /api/usuarios/<id>`, `DELETE /api/usuarios/<id>` |
| Matérias | `GET /api/materias`, `POST /api/materias`, `GET /api/materias/<id>`, `PUT /api/materias/<id>`, `DELETE /api/materias/<id>` |
| Entregas | `GET /api/entregas`, `POST /api/entregas`, `GET /api/entregas/<id>`, `PUT` e `PATCH /api/entregas/<id>`, `DELETE /api/entregas/<id>` |
| Anotações | `GET /api/anotacoes` (filtro opcional `?id_materias=`), `POST /api/anotacoes`, `GET /api/anotacoes/<id>`, `PUT` e `PATCH /api/anotacoes/<id>`, `DELETE /api/anotacoes/<id>`, `POST /api/anotacoes/<id>/imagem`, `GET /api/anotacoes/<id>/imagem` |
| Pomodoro | `GET /api/pomodoro` (filtro opcional `?id_materias=`), `POST /api/pomodoro`, `GET /api/pomodoro/<id>`, `PUT` e `PATCH /api/pomodoro/<id>`, `DELETE /api/pomodoro/<id>` |

A documentação interativa (Swagger) fica disponível em `/apidocs/` com a API em execução.

## 5. Você está usando algum framework para escrever os endpoints da sua API? Se sim, qual?

Sim, **Flask** (Python), na versão 3.1.3. Também são utilizados:

- **Flasgger**, para gerar a documentação Swagger da API;
- **psycopg2**, para a conexão com o banco **PostgreSQL**;
- **python-dotenv**, para ler as variáveis de ambiente do arquivo `.env`;
- **Werkzeug** e **itsdangerous**, para o hash de senhas e a assinatura dos tokens de autenticação.
