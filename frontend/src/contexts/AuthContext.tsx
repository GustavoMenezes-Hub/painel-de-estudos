import { createContext,useCallback,useContext,useEffect,useState,type ReactNode } from 'react';
import { api,tokenStorage } from '../services/api';
import type { Session,User } from '../types/api';

interface AuthValue{user:User|null;checking:boolean;login:(email:string,password:string)=>Promise<void>;logout:()=>void;refresh:()=>Promise<void>}
const AuthContext=createContext<AuthValue|null>(null);
export function AuthProvider({children}:{children:ReactNode}){
 const [user,setUser]=useState<User|null>(null); const [checking,setChecking]=useState(true);
 const logout=useCallback(()=>{tokenStorage.clear();setUser(null)},[]);
 const refresh=useCallback(async()=>{if(!tokenStorage.get()){setUser(null);return} try{setUser(await api<User>('/api/usuarios/me'))}catch(e){if(!tokenStorage.get())setUser(null);throw e}},[]);
 const login=useCallback(async(email:string,password:string)=>{const session=await api<Session>('/api/login',{method:'POST',body:JSON.stringify({email,senha:password})});tokenStorage.set(session.access_token);setUser(session.usuario)},[]);
 useEffect(()=>{refresh().catch(()=>{}).finally(()=>setChecking(false));const expired=()=>setUser(null);window.addEventListener('session:expired',expired);return()=>window.removeEventListener('session:expired',expired)},[refresh]);
 return <AuthContext.Provider value={{user,checking,login,logout,refresh}}>{children}</AuthContext.Provider>
}
export function useAuth(){const value=useContext(AuthContext);if(!value)throw new Error('useAuth deve ser usado dentro de AuthProvider');return value}
