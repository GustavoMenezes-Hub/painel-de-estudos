-- Dados de demonstração para desenvolvimento. Uma conta existente é preservada.
DO $$
DECLARE
    usuario integer;
    adm integer;
    banco integer;
    calculo integer;
    programacao integer;
    nota integer;
BEGIN
    INSERT INTO usuarios (nome, email, senha_hash) VALUES
        ('usuarioteste', 'test123@gmail.com', 'scrypt:32768:8:1$B0J3fb4GoVfJVA5d$cb6ab190b838c34eafe68b88694d0f021f96fe8afa20c39a45bcdb1ad990c5a23a7c75f3da3dc2fa92638b8a0704cf49f01ae4819b564ddfeed88c12d3f3ab74')
        ON CONFLICT DO NOTHING RETURNING id_usuarios INTO usuario;
    IF usuario IS NULL THEN
        RETURN;
    END IF;

    INSERT INTO materias (nome, descricao, id_usuarios) VALUES
        ('Introdução à Administração', 'Fundamentos de administração', usuario) RETURNING id_materias INTO adm;
    INSERT INTO materias (nome, descricao, id_usuarios) VALUES
        ('Banco de dados', 'Modelo relacional e SQL', usuario) RETURNING id_materias INTO banco;
    INSERT INTO materias (nome, descricao, id_usuarios) VALUES
        ('Cálculo B', 'Integrais e aplicações', usuario) RETURNING id_materias INTO calculo;
    INSERT INTO materias (nome, descricao, id_usuarios) VALUES
        ('Programação B', 'JavaScript, APIs e arquitetura em camadas', usuario) RETURNING id_materias INTO programacao;
    INSERT INTO materias (nome, descricao, id_usuarios) VALUES
        ('Vetores e Geometria Analítica', 'Vetores, retas e planos', usuario);
    INSERT INTO entregas (titulo, data_vencimento, id_materias) VALUES
        ('Trabalho 1', '2026-10-30', adm), ('Projeto de Banco de Dados', '2026-11-10', banco),
        ('Lista de integrais', '2026-10-25', calculo), ('Projeto Painel de Estudos', '2026-11-20', programacao);
    INSERT INTO anotacoes (texto, situacao, id_materias) VALUES
        ('Revisar modelo relacional e chaves estrangeiras', 'pendente_revisao', banco) RETURNING id_anotacoes INTO nota;
    INSERT INTO anotacoes (texto, situacao, id_materias) VALUES
        ('Estudar CRUD e arquitetura em camadas', 'iniciar_estudo', programacao),
        ('Revisar integrais definidas', 'estudada', calculo);
    INSERT INTO pomodoro (inicio, duracao_foco_min, duracao_pausa_min, tipo, concluida, id_materias, id_anotacoes) VALUES
        ('2026-10-15 14:00:00-03', 25, 5, 'foco', TRUE, banco, nota),
        ('2026-10-15 15:00:00-03', 25, 5, 'foco', TRUE, programacao, NULL);
END $$;
