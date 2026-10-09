CREATE TABLE materias (
    id_materias INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    id_usuarios INTEGER NOT NULL,
    CONSTRAINT fk_usuario_materias FOREIGN KEY (id_usuarios)
      REFERENCES usuarios(id_usuarios)
);
