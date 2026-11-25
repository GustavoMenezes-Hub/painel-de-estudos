# Painel de Estudos - Frontend

Base compartilhada em React + TypeScript + Vite para a entrega do Integrante 1.

## Executar

1. Inicie o backend Flask na porta `3000`.
2. Nesta pasta, execute `npm install`.
3. Execute `npm run dev` e abra `http://localhost:5173`.

O Vite encaminha automaticamente chamadas `/api` para `http://127.0.0.1:3000`.

## Estrutura compartilhada

- `services/api.ts`: único cliente HTTP, token Bearer e erros.
- `contexts/AuthContext.tsx`: login, validação de sessão e logout.
- `routes/ProtectedRoute.tsx`: bloqueio de páginas sem sessão.
- `layouts/AppLayout.tsx`: menu, cabeçalho e área de conteúdo.
- `components`: campos, avisos e marca reutilizáveis.
- `styles/global.css`: tokens e estilos responsivos.

As áreas Painel, Matérias, Entregas, Anotações e Pomodoro estão com páginas provisórias para os integrantes 2 e 3 substituírem sem alterar a estrutura de sessão e navegação.
