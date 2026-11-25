import type { ApiErrorBody } from '../types/api';

const TOKEN_KEY='painel_estudos_token';
export const tokenStorage={get:()=>localStorage.getItem(TOKEN_KEY),set:(v:string)=>localStorage.setItem(TOKEN_KEY,v),clear:()=>localStorage.removeItem(TOKEN_KEY)};

export class ApiError extends Error { constructor(message:string,public status:number){super(message);this.name='ApiError'} }

export async function api<T=void>(path:string, options:RequestInit={}):Promise<T>{
  const token=tokenStorage.get();
  const headers=new Headers(options.headers);
  if(options.body) headers.set('Content-Type','application/json');
  if(token) headers.set('Authorization',`Bearer ${token}`);
  let response:Response;
  try { response=await fetch(path,{...options,headers}); }
  catch { throw new ApiError('Não foi possível conectar ao servidor. Verifique se o backend está em execução.',0); }
  if(!response.ok){
    let body:ApiErrorBody={}; try{body=await response.json()}catch{/* resposta sem JSON */}
    if(response.status===401 && token){ tokenStorage.clear(); window.dispatchEvent(new Event('session:expired')); }
    const fallback=response.status===503?'O serviço está temporariamente indisponível. Tente novamente em instantes.':`A operação não pôde ser concluída (${response.status}).`;
    throw new ApiError(body.erro||body.mensagem||fallback,response.status);
  }
  if(response.status===204) return undefined as T;
  return response.json() as Promise<T>;
}
