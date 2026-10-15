CREATE TABLE anotacoes (
    id_anotacoes INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    texto TEXT NOT NULL,
    situacao VARCHAR(30) NOT NULL DEFAULT 'pendente_revisao'
        CONSTRAINT chk_situacao_anotacao CHECK (situacao IN ('pendente_revisao', 'iniciar_estudo', 'estudada')),
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    id_materias INTEGER NOT NULL,
    CONSTRAINT fk_anotacoes_materias FOREIGN KEY (id_materias)
      REFERENCES materias(id_materias)
);