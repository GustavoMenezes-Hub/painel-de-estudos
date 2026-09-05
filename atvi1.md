Atividade 1 

1. Quais tabelas você definiu inicialmente?

Três tabelas: materias, entregas e notas.

2. Você utilizou migrations? Se sim, quantas migrations? Descreva em uma frase o que cada uma faz.

Sim, três migrations:

001_create_materias: cria a tabela materias, responsável por armazenar as disciplinas cadastradas pelo usuário.
002_create_entregas: cria a tabela entregas, armazenando as atividades vinculadas a uma matéria, com foreign key materia_id referenciando materias.
003_create_notas: cria a tabela notas, armazenando anotações vinculadas a uma matéria e, opcionalmente, a uma entrega específica, com foreign keys para materias e entregas.

3. Qual o caminho do arquivo que gera a seed do seu banco?

backend/seed.sql

4. Quais os endpoints que você irá implementar inicialmente? Cada endpoint deve ser um método e um path. Explique em um parágrafo por que você resolveu priorizar a implementação desses endpoints.

GET /api/materias
POST /api/materias
GET /api/materias/<id>/entregas
POST /api/entregas
GET /api/notas

Esses foram os endpoints priorizados porque representam as operações primárias da aplicação: são os primeiros dados solicitados assim que o usuário abre o programa — as matérias, suas entregas e as notas associadas a cada uma. Sem esses endpoints básicos de listagem e criação, nenhuma outra funcionalidade do painel consegue funcionar, já que todas dependem desses três recursos existirem primeiro.

5. Você está usando algum framework para escrever os endpoints da sua API? Se sim, qual?

Sim, Flask (Python).