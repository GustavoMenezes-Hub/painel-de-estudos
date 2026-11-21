from contextlib import closing
from pathlib import Path

from src.db import get_connection


def popular(conexao):
    """Carrega a conta fictícia e seus exemplos a partir de seed.sql."""
    with conexao, conexao.cursor() as cursor:
        cursor.execute(Path(__file__).with_suffix(".sql").read_text(encoding="utf-8"))


if __name__ == "__main__":
    with closing(get_connection()) as conexao:
        popular(conexao)
    print("Carga de demonstração concluída.")
