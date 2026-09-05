CREATE TABLE notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id INTEGER NOT NULL REFERENCES materias(id),
    entrega_id INTEGER REFERENCES entregas(id),
    texto TEXT NOT NULL,
    situacao TEXT NOT NULL DEFAULT 'pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);