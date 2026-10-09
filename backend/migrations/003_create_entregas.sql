CREATE TABLE entregas (
    id_entregas INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    data_vencimento DATE NOT NULL,
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    situacao VARCHAR(20) NOT NULL DEFAULT 'pendente'
        CONSTRAINT chk_situacao_entrega CHECK (situacao IN ('pendente', 'realizado')),
    id_materias INTEGER NOT NULL,
    CONSTRAINT fk_entregas_materias FOREIGN KEY (id_materias)
      REFERENCES materias(id_materias)
);