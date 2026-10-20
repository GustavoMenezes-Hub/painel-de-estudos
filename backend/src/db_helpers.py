
"""Acesso ao banco: reutiliza get_connection() do projeto."""
from contextlib import contextmanager
from datetime import date, datetime
from src.db import get_connection

@contextmanager
def db_cursor():
    conexao = get_connection()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                yield cursor
    finally:
        conexao.close()

def registro_json(linha):
    if linha is None:
        return None
    resultado = dict(linha)
    for campo, valor in resultado.items():
        if isinstance(valor, (date, datetime)):
            resultado[campo] = valor.isoformat()
    return resultado
