export interface User { id_usuarios:number; nome:string; email:string; data_criacao?:string }
export interface Session { access_token:string; token_type:'Bearer'; expires_in:number; usuario:User }
export interface ApiErrorBody { erro?:string; mensagem?:string }
