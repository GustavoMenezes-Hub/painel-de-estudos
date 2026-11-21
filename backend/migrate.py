import argparse
from contextlib import closing
from getpass import getpass
from pathlib import Path

from werkzeug.security import generate_password_hash

from src.db import get_connection
from src.validacao import MAX_CARACTERES_SENHA

PASTA = Path(__file__).resolve().parent / "migrations"


def recuperar_pendentes(cursor, ler_senha):
    cursor.execute("SELECT id_usuarios, email FROM usuarios WHERE nullif(btrim(senha_hash), '') IS NULL FOR UPDATE")
    for usuario in cursor.fetchall():
        if ler_senha is None:
            raise ValueError("Há contas sem senha. Execute migrate.py --recuperar-contas.")
        senha = ler_senha(usuario["email"])
        if len(senha) < 8:
            raise ValueError("A senha deve ter pelo menos oito caracteres.")
        if len(senha) > MAX_CARACTERES_SENHA:
            raise ValueError(f"A senha deve ter até {MAX_CARACTERES_SENHA} caracteres.")
        cursor.execute("UPDATE usuarios SET senha_hash=%s WHERE id_usuarios=%s",
                       (generate_password_hash(senha), usuario["id_usuarios"]))


def migrar(conexao, ler_senha=None):
    with conexao, conexao.cursor() as cursor:
        # Serializa dois processos iniciados sobre o mesmo banco.
        cursor.execute("SELECT pg_advisory_xact_lock(732641990)")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                arquivo text PRIMARY KEY, aplicado_em timestamptz NOT NULL DEFAULT now()
            )
        """)
        cursor.execute("SELECT arquivo FROM schema_migrations")
        aplicados = {linha["arquivo"] for linha in cursor.fetchall()}
        for arquivo in sorted(PASTA.glob("*.sql")):
            if arquivo.name in aplicados:
                continue
            if arquivo.name == "007_integridade.sql":
                recuperar_pendentes(cursor, ler_senha)
            cursor.execute(arquivo.read_text(encoding="utf-8"))
            cursor.execute("INSERT INTO schema_migrations (arquivo) VALUES (%s)", (arquivo.name,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aplicar migrations do Painel de Estudos.")
    parser.add_argument("--recuperar-contas", action="store_true",
                        help="Definir interativamente uma senha para cada conta legada sem hash.")
    args = parser.parse_args()

    def pedir_senha(email):
        senha = getpass(f"Nova senha para {email}: ")
        if senha != getpass("Confirme a senha: "):
            raise ValueError("As senhas informadas são diferentes.")
        return senha

    with closing(get_connection()) as conexao:
        migrar(conexao, pedir_senha if args.recuperar_contas else None)
    print("Banco atualizado.")
