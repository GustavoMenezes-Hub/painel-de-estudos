# Painel de Estudos

## Resumo do projeto

O **Painel de Estudos** é uma aplicação pessoal para organização acadêmica, pensada para ajudar o estudante a acompanhar matérias, prazos de entregas e sessões de estudo focado. O objetivo é resolver um problema real da rotina universitária: centralizar em um só lugar o que precisa ser entregue, quando, e permitir sessões de estudo produtivas usando a técnica Pomodoro.

O projeto será desenvolvido com:
- **Frontend Web**: HTML, CSS e JavaScript puro
- **Frontend Mobile**: aplicação nativa Android gerada a partir do mesmo código web utilizando **Capacitor**
- **Backend**: Python com **Flask**, expondo uma API REST consumida por ambos os frontends, com persistência em **SQLite**

## Funcionalidades

- **Cadastro de matérias**: o usuário pode criar e gerenciar suas disciplinas
- **Entregas e prazos**: cada matéria pode ter atividades/entregas associadas, com data de vencimento
- **Contagem regressiva**: exibição visual de quantos dias faltam para a próxima entrega
- **Timer Pomodoro**: ciclos de 25 minutos de foco e 5 minutos de pausa (pausa longa a cada 4 ciclos), associados a uma matéria/tarefa específica
- **Notas rápidas por matéria**: espaço para anotações curtas vinculadas a cada disciplina, com três estados possíveis:
  - **Pendente de revisão**: nota marcada para ser revisada depois
  - **Iniciar estudo a partir da nota**: um botão inicia diretamente um Pomodoro vinculado ao assunto da nota
  - **Estudada**: após revisar, a nota é marcada como concluída e sai da lista de pendências, permanecendo no histórico

## Fluxo de uso

1. O usuário cadastra suas matérias (ex: Cálculo A, Discreta, Programação B) e, conforme surgem, as entregas/atividades de cada uma, com data de vencimento.
2. No painel principal, ele visualiza rapidamente todas as matérias com a contagem regressiva da próxima entrega, identificando o que é mais urgente.
3. **Exemplo prático**: durante uma aula, o usuário faz uma anotação rápida vinculada à matéria (ex: "revisar bijetividade antes da prova") e a marca como pendente de revisão. Ao chegar em casa, o painel destaca essa nota entre as pendentes; o usuário toca nela e inicia diretamente uma sessão de Pomodoro para estudar o assunto, com seu material de apoio (livro, PDF, caderno) em mãos.
4. Ao final da sessão de estudo, o usuário marca a nota como estudada, e ela sai da lista de pendências, permanecendo disponível no histórico da matéria.

## Arquitetura

A aplicação segue o modelo cliente-servidor: o backend Flask expõe rotas HTTP (GET/POST/PUT/DELETE) para matérias, entregas e notas, enquanto o frontend (web e mobile) consome essa API via `fetch`. O mesmo código de frontend é reutilizado para gerar a versão mobile nativa através do Capacitor, evitando duplicação de interface entre as duas plataformas.
