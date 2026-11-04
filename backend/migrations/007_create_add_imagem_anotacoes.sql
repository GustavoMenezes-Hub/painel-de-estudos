ALTER TABLE anotacoes
    ADD COLUMN imagem BYTEA,
    ADD COLUMN imagem_tipo VARCHAR(50),
    ADD COLUMN imagem_nome VARCHAR(255),
    ADD CONSTRAINT chk_anotacoes_imagem_tipo CHECK (imagem_tipo IS NULL OR imagem_tipo IN ('image/jpeg', 'image/png', 'image/gif'));