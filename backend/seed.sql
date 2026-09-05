DELETE FROM notas;
DELETE FROM entregas;
DELETE FROM materias;

INSERT INTO materias (NOME) VALUES
    ('introdução a admnistração'),
    ('Banco de dados'),
    ('Calculo B'),
    ('Programação B'),
    ('Vetores e gemotria analítica');
    
INSERT INTO entregas (materia_id, titulo, data_vencimento) VALUES
    (1, 'Trabalho 1', '2026-09-15'),
    (2, 'Projeto de Banco de Dados', '2026-10-20');

INSERT INTO notas (materia_id, entrega_id, texto, situacao) VALUES
    (1, 1, 'Trabalho em andamento.', 'pendente'),
    (2, 2, 'Projeto concluído com sucesso.', 'aprovado');