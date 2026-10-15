TRUNCATE usuarios, materias, entregas, anotacoes, pomodoro
    RESTART IDENTITY CASCADE;

INSERT INTO usuarios (nome, email) VALUES
    ('Gustavo', 'gustavo@email.com');

INSERT INTO materias (nome, descricao, id_usuarios) VALUES
    ('Introdução à Administração', 'Fundamentos de administração', 1),
    ('Banco de dados', 'Modelo relacional e SQL', 1),
    ('Cálculo B', 'Integrais e aplicações', 1),
    ('Programação B', 'JavaScript, APIs e arquitetura em camadas', 1),
    ('Vetores e Geometria Analítica', 'Vetores, retas e planos', 1);

INSERT INTO entregas (titulo, data_vencimento, id_materias) VALUES
    ('Trabalho 1', '2026-10-30', 1),
    ('Projeto de Banco de Dados', '2026-11-10', 2),
    ('Lista de integrais', '2026-10-25', 3),
    ('Projeto Painel de Estudos', '2026-11-20', 4);

INSERT INTO anotacoes (texto, situacao, id_materias) VALUES
    ('Revisar modelo relacional e chaves estrangeiras', 'pendente_revisao', 2),
    ('Estudar CRUD e arquitetura em camadas', 'iniciar_estudo', 4),
    ('Revisar integrais definidas', 'estudada', 3);

INSERT INTO pomodoro (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes) VALUES
    ('2026-10-15 14:00:00-03', 25, 5, 'foco', TRUE, 2, 1),
    ('2026-10-15 15:00:00-03', 25, 5, 'foco', TRUE, 4, NULL);