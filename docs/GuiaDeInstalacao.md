# Guia de Instalação — Painel de Estudos

Este guia explica como instalar e executar o backend do **Painel de Estudos** (Flask + PostgreSQL) em uma máquina local.

## 1. Pré-requisitos

- **Python 3.13** (versão usada no desenvolvimento; o Flask 3.1 também funciona em versões 3.9 ou superiores)
- **PostgreSQL** instalado e em execução
- **Git**

## 2. Obter o projeto

```bash
git clone https://github.com/GustavoMenezes-Hub/painel-de-estudos.git
cd painel-de-estudos
git checkout entrega1
```

Se você recebeu o projeto em um arquivo ZIP, basta extraí-lo e entrar na pasta extraída, que contém as pastas `backend` e `docs`.

## 3. Criar o ambiente virtual e instalar as dependências

Todos os comandos a seguir devem ser executados dentro da pasta `backend`.

```bash
cd backend
python -m venv .venv
```

Ativar o ambiente virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

## 4. Criar o banco de dados

No PostgreSQL, crie um banco vazio com o nome `painel_estudos`. Pelo terminal:

```bash
psql -U postgres -c "CREATE DATABASE painel_estudos;"
```

Ou pelo **pgAdmin**: clique com o botão direito em *Databases*, escolha *Create > Database* e informe o nome `painel_estudos`.

## 5. Configurar o arquivo `.env`

Copie o arquivo de exemplo e edite os valores:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Conteúdo do `.env`:

```env
DATABASE_URL=postgresql://postgres:SENHA_DO_SEU_POSTGRES@localhost:5432/painel_estudos
SECRET_KEY=SUBSTITUA_POR_UMA_CHAVE_SECRETA_FORTE
```

- Troque `SENHA_DO_SEU_POSTGRES` pela senha do seu usuário do PostgreSQL.
- Troque `SECRET_KEY` por uma chave longa e aleatória. Para gerar uma:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

A aplicação **não inicia** sem a `SECRET_KEY`. O arquivo `.env` está no `.gitignore` e não deve ser enviado ao repositório.

## 6. Criar as tabelas (migrations)

Ainda dentro da pasta `backend`:

```bash
python migrate.py
```

O script executa as migrations `001` a `007` em ordem. Ao final, deve aparecer `migrations concluídas.`

> As migrations usam `CREATE TABLE` sem `IF NOT EXISTS`, então não podem ser executadas duas vezes no mesmo banco. Para recomeçar do zero, apague e recrie o banco (passo 4) e rode `python migrate.py` novamente.

## 7. Popular o banco com dados de exemplo (opcional)

```bash
python seed.py
```

Ao final, deve aparecer `seed concluído.` O script **apaga todos os dados** das tabelas antes de inserir os de exemplo.

O seed cria o usuário de teste abaixo:

| Campo | Valor |
|---|---|
| Nome | Gustavo |
| E-mail | `gustavo@email.com` |
| Senha | `Gustavo123` |

Se preferir, você também pode criar um usuário novo pela API (passo 9).

## 8. Executar a API

Ainda na pasta `backend`:

```bash
python -m src.app
```

A API fica disponível em `http://localhost:3000`, e a documentação interativa (Swagger) em:

```
http://localhost:3000/apidocs/
```

Outra forma de iniciar, equivalente à anterior:

```bash
python -m flask --app src.app run --port 3000
```

> Não use `python src/app.py`, porque o projeto importa seus módulos a partir do pacote `src`.

Para ativar o modo debug com o primeiro comando, defina antes a variável `FLASK_DEBUG=1`. O servidor precisa permanecer em execução enquanto os testes forem realizados.

## 9. Testar a API

### 9.1 Pelo Swagger (recomendado)

1. Acesse `http://localhost:3000/apidocs/`.
2. Abra `POST /api/login` e clique em **Try it out**.
3. Informe o e-mail e a senha do usuário de teste (passo 7) e clique em **Execute**.
4. Copie o valor de `access_token` da resposta.
5. Clique em **Authorize** e informe o token no formato `Bearer SEU_TOKEN`.
6. Teste as rotas protegidas. O Swagger mostra os parâmetros, exemplos de requisição e respostas de cada operação.

### 9.2 Pelo terminal (curl)

Abra outro terminal e siga os passos abaixo. No Windows PowerShell, use `curl.exe` no lugar de `curl`, ou então teste tudo pelo Swagger.

**Criar um usuário** (senha com no mínimo 8 caracteres):

```bash
curl -X POST http://localhost:3000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Seu Nome", "email": "voce@email.com", "senha": "senha12345"}'
```

**Fazer login** e copiar o valor de `access_token` da resposta:

```bash
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "voce@email.com", "senha": "senha12345"}'
```

**Listar as matérias** usando o token:

```bash
curl http://localhost:3000/api/materias \
  -H "Authorization: Bearer SEU_TOKEN"
```

O token é válido por 24 horas.

## 10. Estrutura de pastas

```
painel-de-estudos/
├── README.md
├── ativ1.md
├── guia_instalacao.md
├── docs/                  # modelagem do projeto
└── backend/
    ├── migrations/        # scripts SQL 001 a 007
    ├── src/
    │   ├── app.py         # ponto de entrada da API
    │   ├── db.py          # conexão com o PostgreSQL
    │   ├── auth/          # login e verificação do token
    │   ├── usuarios/
    │   ├── materias/
    │   ├── entregas/
    │   ├── anotacoes/
    │   └── pomodoro/      # cada pasta: route, controller, service e repository
    ├── migrate.py         # executa as migrations
    ├── seed.py / seed.sql # dados de exemplo
    ├── requirements.txt
    └── .env.example
```

## 11. Problemas comuns

| Problema | Causa provável | Solução |
|---|---|---|
| `Configure SECRET_KEY no arquivo .env local antes de iniciar o Flask` | `.env` ausente ou sem `SECRET_KEY` | Crie o `.env` a partir do `.env.example` (passo 5). |
| `KeyError: 'DATABASE_URL'` | `.env` ausente ou fora da pasta `backend` | Confirme que o `.env` está em `backend/` e que você executa os comandos nessa pasta. |
| `password authentication failed` | Senha do PostgreSQL incorreta na `DATABASE_URL` | Corrija a senha no `.env`. |
| `database "painel_estudos" does not exist` | Banco não criado | Execute o passo 4. |
| `relation "usuarios" already exists` | Migrations já executadas | Recrie o banco (passo 4) e rode `python migrate.py` de novo. |
| `ModuleNotFoundError: No module named 'src'` | API iniciada com `python src/app.py` | Use `python -m src.app` dentro de `backend/`. |
| `401 Token Bearer obrigatório` | Requisição sem o cabeçalho `Authorization` | Faça login e envie `Authorization: Bearer SEU_TOKEN`. |

## 12. Limitações conhecidas

- **Upload de imagem em anotações:** a API aceita arquivos PNG, JPEG e WEBP (limite de 5 MB), mas a restrição criada pela migration 007 aceita apenas `image/jpeg`, `image/png` e `image/gif` no banco. Por isso, o envio de uma imagem **WEBP** é recusado com o erro `Dados violam uma regra do banco`. Use PNG ou JPEG até que código e migration sejam alinhados.
- **Seed:** o `seed.py` apaga todos os registros das cinco tabelas. Execute-o somente em um banco local de testes.
