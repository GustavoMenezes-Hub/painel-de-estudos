export interface User { id_usuarios:number; nome:string; email:string; data_criacao?:string }
export interface Session { access_token:string; token_type:'Bearer'; expires_in:number; usuario:User }
export interface ApiErrorBody { erro?:string; mensagem?:string }

export interface Materia {
  id_materias: number;
  nome: string;
  descricao: string | null;
}

export interface DadosEntrega {
  titulo: string;
  id_materias: number;
  data_vencimento: string;
  situacao: 'pendente' | 'realizado';
}

export interface Entrega extends DadosEntrega {
  id_entregas: number;
}
