"""Testes com uma base PostgreSQL nova por execução. Rodar a partir de backend/."""
import os
import re
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timezone
from threading import Barrier, Thread
from unittest.mock import patch
from urllib.request import urlopen
from uuid import uuid4

import psycopg2
from psycopg2 import errors, sql
from psycopg2.extensions import make_dsn
from werkzeug.security import check_password_hash
from werkzeug.serving import make_server

from migrate import migrar, PASTA
from seed import popular
from src.db import get_connection


class BackendPostgres(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = os.environ["DATABASE_URL"]
        nome = "painel_teste_" + uuid4().hex
        admin = psycopg2.connect(base, connect_timeout=5)
        cls.addClassCleanup(admin.close)
        admin.autocommit = True
        with admin.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0").format(sql.Identifier(nome)))

        def remover_banco_criado():
            with admin.cursor() as cursor:
                cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(nome)))

        cls.addClassCleanup(remover_banco_criado)
        config = patch.dict(os.environ, DATABASE_URL=make_dsn(base, dbname=nome), SECRET_KEY=uuid4().hex)
        config.start()
        cls.addClassCleanup(config.stop)
        with closing(get_connection()) as conexao:
            with conexao, conexao.cursor() as cursor:
                cursor.execute("SELECT current_database() AS nome")
                assert cursor.fetchone()["nome"] == nome
            migrar(conexao)
            migrar(conexao)
        from src.app import app
        cls.app = app

    def setUp(self):
        self.client = self.app.test_client()
        self.senha = "Senha de teste 42"
        self.email = uuid4().hex + "@example.org"
        self.usuario, self.token = self.conta(self.email)

    def api(self, metodo, rota, esperado, dados=None, token=None):
        cabecalhos = {"Authorization": "Bearer " + token} if token else {}
        resp = self.client.open("/api/" + rota, method=metodo, json=dados, headers=cabecalhos)
        self.assertEqual(resp.status_code, esperado, (metodo, rota, resp.get_json(silent=True)))
        return resp.get_json(silent=True)

    def conta(self, email):
        usuario = self.api("POST", "usuarios", 201, {"nome": "Estudante", "email": email, "senha": self.senha})
        sessao = self.api("POST", "login", 200, {"email": email.upper(), "senha": self.senha})
        self.assertNotIn("senha_hash", usuario)
        self.assertEqual(sessao["usuario"]["id_usuarios"], usuario["id_usuarios"])
        return usuario, sessao["access_token"]

    def materia(self, nome="Estudos", token=None):
        return self.api("POST", "materias", 201, {"nome": nome}, token or self.token)["id_materias"]

    def test_conta_permissoes_e_troca_de_senha(self):
        rota = "usuarios/" + str(self.usuario["id_usuarios"])
        self.assertEqual(self.api("GET", rota, 200, token=self.token), self.usuario)
        self.assertEqual(self.api("GET", "usuarios/me", 200, token=self.token), self.usuario)
        _, outro = self.conta(uuid4().hex + "@example.org")
        for metodo in ("GET", "PATCH", "DELETE"):
            self.api(metodo, rota, 403, {"nome": "Outro"} if metodo == "PATCH" else None, outro)
        resumo = self.api("GET", "usuarios", 200, token=self.token)
        self.assertEqual(resumo, [{"nome": "Estudante", "id_usuarios": self.usuario["id_usuarios"]}])
        self.api("POST", "usuarios", 409, {"nome":"Duplicado", "email":self.email.upper(), "senha":self.senha})
        with closing(get_connection()) as conn, conn.cursor() as c:
            c.execute("SELECT senha_hash FROM usuarios WHERE email=%s",(self.email,))
            self.assertTrue(check_password_hash(c.fetchone()["senha_hash"], self.senha))
        self.api("GET", "usuarios/me", 401)
        self.api("GET", "usuarios/me", 401, token="invalido")
        self.api("PUT", rota, 200, {"nome": "Nome atualizado"}, self.token)
        self.api("PATCH", rota, 200, {"senha": "Uma nova senha"}, self.token)
        self.api("GET", "usuarios/me", 401, token=self.token)
        self.api("POST", "login", 401, {"email": self.email, "senha": self.senha})
        novo = self.api("POST", "login", 200, {"email": self.email, "senha": "Uma nova senha"})["access_token"]
        self.api("DELETE", rota, 204, token=novo)
        self.api("GET", "usuarios/me", 401, token=novo)

    def test_ciclo_completo_dos_recursos(self):
        t = self.token
        mid = self.materia()
        materia = f"materias/{mid}"
        self.api("GET", materia, 200, token=t)
        self.api("PUT", materia, 200, {"nome":"Nova", "descricao":"Descrição"}, t)
        self.assertEqual(len(self.api("GET","materias",200,token=t)),1)
        self.api("DELETE","usuarios/" + str(self.usuario["id_usuarios"]),409,token=t)
        entrega = self.api("POST","entregas",201,{"id_materias":mid,"titulo":"Lista","data_vencimento":"2026-11-27"},t)
        e = "entregas/" + str(entrega["id_entregas"])
        self.assertEqual(self.api("GET",materia+"/entregas",200,token=t),[entrega])
        self.api("PATCH",e,200,{"situacao":"realizado"},t)
        nota = self.api("POST","anotacoes",201,{"id_materias":mid,"texto":"Revisar"},t)
        n = "anotacoes/" + str(nota["id_anotacoes"])
        self.assertEqual(self.api("GET",f"notas?id_materias={mid}",200,token=t),[nota])
        self.api("PATCH",n,200,{"situacao":"estudada"},t)
        sessao = self.api("POST","pomodoro",201,{"id_materias":mid,"id_anotacoes":nota["id_anotacoes"],
                          "inicio":"2026-11-20T12:00:00Z","duracao_foco_min":25,"duracao_pausa_min":5},t)
        p = "pomodoro/" + str(sessao["id_pomodoro"])
        self.api("PATCH",p,200,{"concluida":True},t)
        self.api("PATCH",n,409,{"id_materias":self.materia("Outra")},t)
        for rota, item, campos in [("entregas",e,{"titulo":"Revisão"}),("anotacoes",n,{"texto":"Texto"}),
                                   ("pomodoro",p,{"tipo":"Foco"})]:
            self.api("GET",item,200,token=t)
            self.assertEqual(len(self.api("GET",rota,200,token=t)),1)
            self.api("PUT",item,200,campos,t)
        self.api("DELETE",n,200,token=t)
        self.assertIsNone(self.api("GET",p,200,token=t)["id_anotacoes"])
        self.api("DELETE",p,200,token=t)
        self.api("DELETE",e,204,token=t)
        self.api("DELETE",materia,204,token=t)
        for item in (materia,e,n,p):
            self.api("GET",item,404,token=t)

    def test_isolamento_dos_estudantes_e_cascata(self):
        _, outro = self.conta(uuid4().hex + "@example.org")
        da_conta = self.materia()
        de_outro = self.materia(token=outro)
        dados = {"id_materias":da_conta, "titulo":"Lista","data_vencimento":"2026-11-27"}
        self.api("POST","entregas",404,dados,outro)
        self.api("GET",f"materias/{da_conta}/entregas",404,token=outro)
        entrega = self.api("POST","entregas",201,dados,self.token)
        item = "entregas/"+str(entrega["id_entregas"])
        self.api("PATCH",item,404,{"id_materias":de_outro},self.token)
        self.api("GET",item,404,token=outro)
        self.api("DELETE",item,404,token=outro)
        nota = self.api("POST","anotacoes",201,{"texto":"A","id_materias":da_conta},self.token)
        nid = nota["id_anotacoes"]
        self.api("GET",f"anotacoes/{nid}",404,token=outro)
        dados = {"id_materias":de_outro,"id_anotacoes":nid,"inicio":"2026-11-18T12:00:00Z",
                 "duracao_foco_min":1,"duracao_pausa_min":0}
        self.api("POST","pomodoro",404,dados,outro)
        sessao = self.api("POST","pomodoro",201,{**dados,"id_materias":da_conta},self.token)
        pid = sessao["id_pomodoro"]
        self.api("DELETE",f"pomodoro/{pid}",404,token=outro)
        self.api("DELETE",f"materias/{da_conta}",204,token=self.token)
        for path in (item,f"anotacoes/{nid}",f"pomodoro/{pid}"):
            self.api("GET",path,404,token=self.token)

    def test_validacoes_http(self):
        for rota, valores in [
            ("materias", {"nome":" "}), ("materias", {"nome":"a"*101}),
            ("anotacoes", {"texto":"x", "id_materias":True}),
            ("entregas", {"titulo":"Atividade", "data_vencimento":"2026-02-30"}),
            ("pomodoro", {"inicio":"2026-11-18"}),
            ("usuarios", {"nome":"A","email":"@example.org","senha":self.senha}),
            ("usuarios", {"nome":"A","email":self.email,"senha":"curta"}),
        ]:
            with self.subTest(rota=rota):
                self.api("POST",rota,400,valores,self.token)
        for rota in ("pomodoro","anotacoes","notas"):
            self.api("GET",rota+"?id_materias=invalido",400,token=self.token)
        self.api("GET","materias/2147483648",400,token=self.token)
        self.api("GET","ausente",404)
        resposta = self.client.post("/api/usuarios/me")
        self.assertEqual(resposta.status_code,405)
        self.assertIn("GET",resposta.headers["Allow"])

    def test_integridade_direta_e_rollback(self):
        mid = self.materia()
        outro = self.materia()
        nota = self.api("POST","anotacoes",201,{"texto":"Nota","id_materias":mid},self.token)
        with closing(get_connection()) as conn:
            with self.assertRaises(errors.ForeignKeyViolation), conn, conn.cursor() as c:
                c.execute("""INSERT INTO pomodoro(inicio,duracao_foco_min,duracao_pausa_min,id_materias,id_anotacoes)
                             VALUES(now(),25,5,%s,%s)""",(outro,nota["id_anotacoes"]))
            with self.assertRaises(errors.UniqueViolation), conn, conn.cursor() as c:
                c.execute("INSERT INTO usuarios(nome,email,senha_hash) VALUES('Teste',%s,'teste')",(self.email.upper(),))
            with self.assertRaises(errors.NotNullViolation), conn, conn.cursor() as c:
                c.execute("INSERT INTO usuarios(nome,email) VALUES('Teste','sem-hash@example.org')")
            with conn, conn.cursor() as c:
                c.execute("SELECT count(*) AS n FROM pomodoro WHERE id_materias=%s",(outro,))
                self.assertEqual(c.fetchone()["n"],0)

    def test_concorrencia_atualizacoes_e_vinculo(self):
        mid = self.materia()
        outro = self.materia()
        nota = self.api("POST","anotacoes",201,{"texto":"Nota","id_materias":mid},self.token)
        nid = nota["id_anotacoes"]
        item = f"/api/anotacoes/{nid}"
        def simultaneas(operacoes):
            inicio = Barrier(len(operacoes))
            def chamada(operacao):
                metodo, rota, dados = operacao
                with self.app.test_client() as cliente:
                    inicio.wait(timeout=10)
                    return cliente.open(rota,method=metodo,json=dados,
                                        headers={"Authorization":"Bearer "+self.token}).status_code
            with ThreadPoolExecutor(max_workers=len(operacoes)) as executor:
                return list(executor.map(chamada,operacoes))
        self.assertEqual(simultaneas([("PATCH",item,{"texto":"Alterada"}),
                                      ("PATCH",item,{"situacao":"estudada"})]),[200,200])
        atual = self.api("GET",f"anotacoes/{nid}",200,token=self.token)
        self.assertEqual((atual["texto"],atual["situacao"]),("Alterada","estudada"))
        sessao = {"id_materias":mid,"id_anotacoes":nid,"inicio":"2026-11-18T12:00:00Z",
                  "duracao_foco_min":1,"duracao_pausa_min":0}
        resultado = simultaneas([("PATCH",item,{"id_materias":outro}),("POST","/api/pomodoro",sessao)])
        self.assertIn(resultado,([409,201],[200,404]))

    def test_migracao_de_conta_legada(self):
        with closing(get_connection()) as conn:
            with conn, conn.cursor() as c:
                c.execute("CREATE SCHEMA legado")
                c.execute("SET search_path TO legado")
                for arquivo in sorted(PASTA.glob("*.sql"))[:5]:
                    c.execute(arquivo.read_text(encoding="utf-8"))
                c.execute("INSERT INTO usuarios (nome,email) VALUES ('Estudante','legado@example.org')")
                c.execute("INSERT INTO materias (nome,id_usuarios) VALUES ('Cálculo',1)")
            with self.assertRaisesRegex(ValueError, "recuperar-contas"):
                migrar(conn)
            with self.assertRaisesRegex(ValueError, "128"):
                migrar(conn, lambda email: "a" * 129)
            migrar(conn, lambda email: self.senha)
            migrar(conn)
            with conn.cursor() as c:
                c.execute("SELECT u.id_usuarios,u.senha_hash,m.nome FROM usuarios u JOIN materias m USING (id_usuarios)")
                antigo = c.fetchone()
                self.assertTrue(check_password_hash(antigo["senha_hash"], self.senha))
                self.assertEqual((antigo["id_usuarios"], antigo["nome"]), (1, "Cálculo"))

    def test_expiracao_do_token(self):
        from time import time
        with patch("itsdangerous.timed.time.time", return_value=time() + 86401):
            self.api("GET", "usuarios/me", 401, token=self.token)

    def test_seed_repetida_e_migrations(self):
        with closing(get_connection()) as conn:
            for _ in range(2):
                migrar(conn)
                popular(conn)
            with conn.cursor() as c:
                c.execute("SELECT count(*) AS n FROM schema_migrations")
                self.assertEqual(c.fetchone()["n"],len(list(PASTA.glob("*.sql"))))
        credenciais = {"email": "test123@gmail.com", "senha": "Test1234!"}
        sessao = self.api("POST", "login", 200, credenciais)
        token_demo = sessao["access_token"]
        perfil = self.api("GET", "usuarios/me", 200, token=token_demo)
        self.assertEqual(perfil["nome"], "usuarioteste")
        self.assertEqual(perfil["email"], credenciais["email"])
        for rota, quantidade in [("materias", 5), ("entregas", 4), ("anotacoes", 3), ("pomodoro", 2)]:
            with self.subTest(rota=rota):
                self.assertEqual(len(self.api("GET", rota, 200, token=token_demo)), quantidade)
        outro_perfil = f"usuarios/{self.usuario['id_usuarios']}"
        self.api("GET", outro_perfil, 403, token=token_demo)
        self.assertEqual(self.api("GET", "usuarios/me", 200, token=self.token), self.usuario)

    def test_servidor_http_e_contrato(self):
        servidor = make_server("127.0.0.1",0,self.app)
        thread = Thread(target=servidor.serve_forever)
        thread.start()
        try:
            import json
            with urlopen(f"http://127.0.0.1:{servidor.server_port}/apispec_1.json",timeout=5) as r:
                spec = json.load(r)
        finally:
            servidor.shutdown()
            thread.join()
            servidor.server_close()
        rotas = {(re.sub(r"<int:(\w+)>",r"{\1}",regra.rule),metodo.lower())
                 for regra in self.app.url_map.iter_rules() if regra.rule.startswith("/api/")
                 for metodo in regra.methods - {"HEAD","OPTIONS"}}
        documentadas = {(rota,metodo) for rota,metodos in spec["paths"].items() for metodo in metodos}
        self.assertEqual(documentadas,rotas)
        self.assertEqual(len(documentadas), 33)
        grupos = {op["tags"][0] for metodos in spec["paths"].values() for op in metodos.values()}
        self.assertEqual(grupos, {"Autenticação", "Usuários", "Matérias", "Entregas", "Anotações", "Pomodoro"})
        for rota, metodo in rotas:
            operacao = spec["paths"][rota][metodo]
            publica = (rota,metodo) in {("/api/login","post"),("/api/usuarios","post")}
            self.assertEqual(bool(operacao["security"]),not publica)
            self.assertTrue(operacao["responses"])

    def test_pomodoro_instante_em_fusos_diferentes(self):
        dados = {"id_materias": self.materia(), "duracao_foco_min": 25, "duracao_pausa_min": 5}
        esperado = datetime(2026, 11, 21, 15, tzinfo=timezone.utc)
        base = os.environ["DATABASE_URL"]
        casos = [("UTC", "2026-11-21T15:00:00Z"),
                 ("America/Fortaleza", "2026-11-21T12:00:00-03:00"),
                 ("Asia/Kathmandu", "2026-11-21T20:45:00+05:45")]
        rotas = []
        for fuso, inicio in casos:
            dsn = make_dsn(base, options=f"-c timezone={fuso}")
            with self.subTest(fuso=fuso), patch.dict(os.environ, DATABASE_URL=dsn):
                criado = self.api("POST", "pomodoro", 201, {**dados, "inicio": inicio}, self.token)
                self.assertEqual(datetime.fromisoformat(criado["inicio"]), esperado)
                rotas.append(f"pomodoro/{criado['id_pomodoro']}")
                with closing(get_connection()) as conn, conn.cursor() as c:
                    c.execute("SELECT current_setting('TimeZone') AS fuso, extract(epoch FROM inicio) AS instante "
                              "FROM pomodoro WHERE id_pomodoro = %s", (criado["id_pomodoro"],))
                    linha = c.fetchone()
                    self.assertEqual(linha["fuso"], fuso)
                    self.assertEqual(linha["instante"], esperado.timestamp())
                for rota in rotas:
                    lido = self.api("GET", rota, 200, token=self.token)
                    self.assertEqual(datetime.fromisoformat(lido["inicio"]), esperado)
        novo_inicio = "2026-11-22T00:05:10.123456+05:45"
        atualizado = self.api("PATCH", rotas[0], 200, {"inicio": novo_inicio}, self.token)
        self.assertEqual(datetime.fromisoformat(atualizado["inicio"]), datetime.fromisoformat(novo_inicio))
        with patch.dict(os.environ, DATABASE_URL=make_dsn(base, options="-c timezone=America/Fortaleza")):
            mantido = self.api("PUT", rotas[0], 200, {"concluida": True}, self.token)
            self.assertEqual(datetime.fromisoformat(mantido["inicio"]), datetime.fromisoformat(novo_inicio))

    def test_pomodoro_rejeita_inicio_invalido_ou_sem_fuso(self):
        dados = {"id_materias": self.materia(), "duracao_foco_min": 25, "duracao_pausa_min": 0}
        criado = self.api("POST", "pomodoro", 201, {**dados, "inicio": "2026-11-21T15:00:00Z"}, self.token)
        rota = f"pomodoro/{criado['id_pomodoro']}"
        for inicio in ("2026-11-21T12:00:00", "2026-11-21", "2026-02-30T12:00:00Z",
                       "2026-11-21T12:00:00-03:60", "2026-11-21T12:00:00+24:00",
                       "2026-11-21X12:00:00Z", "inválido", None):
            for metodo, destino in (("POST", "pomodoro"), ("PUT", rota), ("PATCH", rota)):
                with self.subTest(inicio=inicio, metodo=metodo):
                    erro = self.api(metodo, destino, 400, {**dados, "inicio": inicio}, self.token)
                    self.assertIn("inicio", erro["erro"])
        self.assertEqual(self.api("GET", rota, 200, token=self.token), criado)

    def test_limite_do_texto_de_anotacao(self):
        dados = {"id_materias": self.materia(), "texto": "á" * 10_000}
        nota = self.api("POST", "anotacoes", 201, dados, self.token)
        self.assertEqual(nota["texto"], dados["texto"])
        rota = f"anotacoes/{nota['id_anotacoes']}"
        for metodo, destino in (("POST", "anotacoes"), ("PUT", rota), ("PATCH", rota)):
            with self.subTest(metodo=metodo):
                erro = self.api(metodo, destino, 400, {**dados, "texto": dados["texto"] + " "}, self.token)
                self.assertIn("texto", erro["erro"])
        self.assertEqual(self.api("GET", rota, 200, token=self.token)["texto"], dados["texto"])
        novo = "ç" * 10_000
        self.assertEqual(self.api("PATCH", rota, 200, {"texto": novo}, self.token)["texto"], novo)

    def test_limite_da_descricao_de_materia(self):
        dados = {"nome": "Estudos", "descricao": "ç" * 2_000}
        materia = self.api("POST", "materias", 201, dados, self.token)
        self.assertEqual(materia["descricao"], dados["descricao"])
        rota = f"materias/{materia['id_materias']}"
        for metodo, destino in (("POST", "materias"), ("PUT", rota)):
            with self.subTest(metodo=metodo):
                erro = self.api(metodo, destino, 400, {**dados, "descricao": " " + dados["descricao"]}, self.token)
                self.assertIn("descricao", erro["erro"])
        self.assertEqual(self.api("GET", rota, 200, token=self.token)["descricao"], dados["descricao"])
        for opcional in ({}, {"descricao": None}, {"descricao": "  "}):
            with self.subTest(opcional=opcional):
                self.assertEqual(self.api("PUT", rota, 200, dados, self.token)["descricao"], dados["descricao"])
                self.assertIsNone(self.api("PUT", rota, 200, {"nome": "Estudos", **opcional}, self.token)["descricao"])

    def test_limite_de_senha_no_cadastro_login_e_alteracao(self):
        senha = " " + "á" * 126 + " "
        email = uuid4().hex + "@example.org"
        dados = {"nome": "Estudante", "email": email, "senha": senha}
        erro = self.api("POST", "usuarios", 400, {**dados, "senha": senha + "a"})
        self.assertIn("128", erro["erro"])
        usuario = self.api("POST", "usuarios", 201, dados)
        login = {"email": email, "senha": senha}
        token = self.api("POST", "login", 200, login)["access_token"]
        self.api("POST", "login", 401, {**login, "senha": senha.strip()})
        self.api("POST", "login", 401, {**login, "senha": "curta"})
        for endereco in (email, uuid4().hex + "@example.org"):
            erro = self.api("POST", "login", 400, {"email": endereco, "senha": senha + "a"})
            self.assertIn("128", erro["erro"])
        rota = f"usuarios/{usuario['id_usuarios']}"
        for metodo in ("PUT", "PATCH"):
            erro = self.api(metodo, rota, 400, {"senha": senha + "a"}, token)
            self.assertIn("128", erro["erro"])
        self.api("GET", "usuarios/me", 200, token=token)
        self.api("POST", "login", 200, login)
        nova = "ü" * 128
        self.api("PATCH", rota, 200, {"senha": nova}, token)
        token = self.api("POST", "login", 200, {**login, "senha": nova})["access_token"]
        self.api("PUT", rota, 400, {"senha": "a" * 7}, token)
        self.api("PUT", rota, 200, {"senha": "a" * 8}, token)
        self.api("POST", "login", 200, {**login, "senha": "a" * 8})

    def test_limite_do_corpo_json_em_bytes(self):
        limite = 1_048_576
        self.assertEqual(self.app.config["MAX_CONTENT_LENGTH"], limite)
        login = self.app.json.dumps({"email": self.email, "senha": self.senha}).encode("utf-8")
        # Espaços após o objeto são JSON válido e contam no corpo transmitido.
        for tamanho, status in ((limite - 1, 200), (limite, 200), (limite + 1, 413)):
            corpo = login.ljust(tamanho, b" ")
            for chunked in (False, True):
                with self.subTest(tamanho=tamanho, chunked=chunked):
                    ambiente = {"HTTP_TRANSFER_ENCODING": "chunked", "wsgi.input_terminated": True} if chunked else {}
                    resp = self.client.post("/api/login", data=corpo, content_type="application/json",
                                            environ_overrides=ambiente)
                    self.assertEqual(resp.status_code, status)
                    self.assertTrue(resp.is_json)
                    if status == 413:
                        self.assertEqual(set(resp.json), {"erro"})
                        self.assertIn("1 MB", resp.json["erro"])
                    else:
                        self.assertIn("access_token", resp.json)
