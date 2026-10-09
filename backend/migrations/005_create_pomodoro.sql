CREATE TABLE pomodoro (
    id_pomodoro INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inicio TIMESTAMPTZ NOT NULL,
    duracao_foco_min INTEGER NOT NULL CHECK (duracao_foco_min > 0),
    duracao_pausa_min INTEGER NOT NULL CHECK (duracao_pausa_min >= 0),
    tipo VARCHAR(50),
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    id_materias INTEGER NOT NULL,
    CONSTRAINT fk_pomodoro_materias FOREIGN KEY (id_materias)
        REFERENCES materias(id_materias)
);