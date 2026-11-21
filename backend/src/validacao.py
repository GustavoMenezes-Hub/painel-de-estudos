from werkzeug.routing import IntegerConverter
from src.api_errors import ApiError

MAX_INTEIRO_POSTGRES = 2_147_483_647
MAX_CARACTERES_SENHA = 128

def id_postgres(valor):
    return type(valor) is int and 0 < valor <= MAX_INTEIRO_POSTGRES

def id_filtro(valor):
    if valor is None:
        return None
    if valor.isdecimal():
        digitos = valor.lstrip("0")
        if 0 < len(digitos) <= 10:
            numero = int(digitos)
            if id_postgres(numero):
                return numero
    raise ApiError("id_materias deve ser inteiro positivo de até 2147483647.")

def validar_texto_postgres(valor, campo, *, maximo=None):
    if isinstance(valor, str):
        if maximo is not None and len(valor) > maximo:
            raise ApiError(f"O campo '{campo}' deve ter até {maximo} caracteres.")
        try:
            valor.encode("utf-8")
        except UnicodeEncodeError:
            raise ApiError(f"{campo} contém caracteres inválidos.") from None
        if "\x00" in valor:
            raise ApiError(f"{campo} contém caracteres inválidos.")

class IdDaRota(IntegerConverter):
    def to_python(self, value):
        digitos = value.lstrip("0") or "0"
        return int(digitos) if len(digitos) <= 10 else MAX_INTEIRO_POSTGRES + 1
