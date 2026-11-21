import unittest

from src.api_errors import ApiError
from src.validacao import id_filtro, id_postgres

class Validacao(unittest.TestCase):
    def test_ids_postgres(self):
        self.assertTrue(id_postgres(2147483647))
        for valor in (True, 0, -1, 2147483648, "1"):
            self.assertFalse(id_postgres(valor))
        self.assertEqual(id_filtro("002"), 2)
        for valor in ("0", "-1", "x", "2147483648"):
            with self.assertRaises(ApiError):
                id_filtro(valor)
