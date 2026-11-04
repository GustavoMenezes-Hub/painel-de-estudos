# Guia de instalação e testes — API Painel de Estudos

Professor, seguem as orientações para executar e testar a API desenvolvida, incluindo a documentação Swagger.

## 1. Acessar o projeto

**Repositório GitHub:** (https://github.com/GustavoMenezes-Hub/painel-de-estudos)

Após baixar ou clonar o projeto, abra a pasta `backend` no VS Code.

## 2. Configurar o ambiente

É necessário ter Python e PostgreSQL instalados.

No terminal PowerShell, dentro da pasta `backend`, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Configurar o banco de dados

No pgAdmin, crie um banco de dados chamado:

```text
painel_estudos
```

Na pasta `backend`, copie o arquivo `.env.example` para um novo arquivo `.env` e configure os dados do PostgreSQL instalado localmente:

```env
SECRET_KEY=SUA_CHAVE_ALEATORIA
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/painel_estudos
```

Substitua `SUA_SENHA` pela senha definida na instalação do PostgreSQL e utilize uma chave privada para `SECRET_KEY`. 

## 4. Criar as tabelas e inserir dados de teste

No terminal, dentro de `backend`, execute:

```powershell
python migrate.py
python seed.py
```

O primeiro comando cria a estrutura do banco de dados. O segundo insere os dados de exemplo.

**Importante:** o `migrate.py` executa todas as migrations (001 a 006) toda vez que roda, então use um banco recém-criado. Se o banco `painel_estudos` já existia de uma versão anterior, apague-o no pgAdmin e crie novamente antes de rodar os comandos acima.

**Atenção:** o `seed.py` executa o `seed.sql`, que limpa e recria os registros das tabelas indicadas. Execute somente no banco local de testes.

## 5. Iniciar a API

Execute:

```powershell
python -m flask --app src.app run --port 3000
```

Com o servidor em execução, acesse a documentação interativa:

**Swagger:** http://localhost:3000/apidocs/

## 6. Dados de acesso para teste

O arquivo `seed.sql` contém o hash da senha do usuário de teste.

- **Usuário:** Gustavo
- **E-mail:** gustavo@email.com
- **Senha:** Gustavo123

## 7. Como testar a API

Na documentação Swagger:

1. Abra **POST `/api/login`**.
2. Clique em **Try it out** e informe o e-mail e a senha acima.
3. Clique em **Execute**.
4. Copie o valor de `access_token` retornado.
5. Clique em **Authorize** e informe o token neste formato:

   ```text
   Bearer SEU_TOKEN
   ```

6. Após autorizar, será possível testar as rotas protegidas documentadas.

### Operações disponíveis na documentação Swagger

| Método | Endpoint | Funcionalidade |
|---|---|---|
| POST | `/api/login` | Autenticação |
| GET | `/api/materias` | Listar matérias |
| POST | `/api/materias` | Cadastrar matéria |
| GET | `/api/materias/{id_materias}` | Consultar matéria |
| PUT | `/api/materias/{id_materias}` | Atualizar matéria |
| DELETE | `/api/materias/{id_materias}` | Excluir matéria |

A documentação apresenta também os parâmetros, exemplos de requisição e respostas HTTP dessas operações.

As demais entidades (usuários, entregas, anotações e Pomodoro) também possuem rotas em `/api/`, mas ainda não estão documentadas no Swagger. Nesta entrega, a documentação cobre o login e o CRUD de matérias.

**Observação:** o servidor precisa permanecer em execução enquanto os testes estiverem sendo realizados.
