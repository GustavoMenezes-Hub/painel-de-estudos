Atividade 1

1. Quais tabelas você definiu inicialmente?

Inicialmente definimos três tabelas: materias, entregas e notas. Com a evolução do projeto, o modelo passou a ter cinco tabelas: usuarios, materias, entregas, anotacoes (que substituiu a tabela notas) e pomodoro.

2. Você utilizou migrations? Se sim, quantas migrations? Descreva em uma frase o que cada uma faz.

Sim. No início eram três migrations (materias, entregas e notas). Hoje o projeto tem seis, todas na pasta backend/migrations:

001_create_usuarios: cria a tabela usuarios, com nome, e-mail único e data de criação.
002_create_materias: cria a tabela materias, vinculada a um usuário por meio da chave estrangeira id_usuarios.
003_create_entregas: cria a tabela entregas, com título, data de vencimento e situação (pendente ou realizado), vinculada a uma matéria.
004_create_anotacoes: cria a tabela anotacoes, com o texto e a situação da anotação, vinculada a uma matéria.
005_create_pomodoro: cria a tabela pomodoro, que registra as sessões de foco e pausa, vinculadas a uma matéria e, opcionalmente, a uma anotação.
006_add_senha_hash: adiciona à tabela usuarios a coluna senha_hash, usada na autenticação.

3. Qual o caminho do arquivo que gera a seed do seu banco?

backend/seed.sql, que é executado pelo script backend/seed.py.

4. Quais os endpoints que você irá implementar inicialmente? Cada endpoint deve ser um método e um path. Explique em um parágrafo por que você resolveu priorizar a implementação desses endpoints.

Os endpoints definidos inicialmente foram:

GET /api/materias
POST /api/materias
GET /api/materias/<id>/entregas
POST /api/entregas
GET /api/notas

Esses endpoints foram priorizados porque representam as operações principais da aplicação: são os primeiros dados que o usuário precisa ver ao abrir o programa, ou seja, as matérias, as entregas e as anotações de cada uma. Sem eles, as demais funcionalidades não teriam como funcionar, já que dependem dessas informações.

Na implementação atual, a API tem os seguintes endpoints:

POST /api/login
POST /api/usuarios
GET /api/usuarios
GET /api/usuarios/me
GET, PUT, PATCH e DELETE /api/usuarios/<id>
GET e POST /api/materias
GET, PUT e DELETE /api/materias/<id>
GET e POST /api/entregas
GET, PUT, PATCH e DELETE /api/entregas/<id>
GET e POST /api/anotacoes
GET, PUT, PATCH e DELETE /api/anotacoes/<id>
GET e POST /api/pomodoro
GET, PUT, PATCH e DELETE /api/pomodoro/<id>

Para a primeira entrega, demos prioridade ao login e ao CRUD de matérias, ambos documentados no Swagger. O login vem primeiro porque todas as rotas, exceto o próprio login e o cadastro de usuário, exigem um token. As matérias vêm em seguida porque entregas, anotações e sessões de Pomodoro estão vinculadas a elas.

5. Você está usando algum framework para escrever os endpoints da sua API? Se sim, qual?

Sim, Flask (Python). A documentação interativa é gerada com o Flasgger (Swagger) e o banco de dados utilizado é o PostgreSQL, acessado pela biblioteca psycopg2.
