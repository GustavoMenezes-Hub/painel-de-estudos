ALTER TABLE usuarios ALTER COLUMN senha_hash SET NOT NULL;
ALTER TABLE usuarios ADD CONSTRAINT chk_senha_preenchida CHECK (btrim(senha_hash) <> '');
ALTER TABLE usuarios ADD COLUMN versao_token integer NOT NULL DEFAULT 1;
CREATE UNIQUE INDEX usuarios_email_normalizado ON usuarios (lower(email));

ALTER TABLE anotacoes ADD CONSTRAINT uq_anotacao_materia UNIQUE (id_anotacoes, id_materias);
ALTER TABLE pomodoro
    DROP CONSTRAINT fk_pomodoro_anotacoes,
    ADD CONSTRAINT fk_pomodoro_anotacao_materia
        FOREIGN KEY (id_anotacoes, id_materias) REFERENCES anotacoes (id_anotacoes, id_materias)
        ON DELETE SET NULL (id_anotacoes);
