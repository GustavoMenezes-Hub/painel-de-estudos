import { Camera,UserRound } from 'lucide-react';
import { useEffect,useState,type ChangeEvent } from 'react';
import type { User } from '../types/api';

const key=(id:number)=>`painel_estudos_avatar_${id}`;
export function UserAvatar({user,editable=false}:{user:User|null;editable?:boolean}){
 const [src,setSrc]=useState<string|null>(()=>user?localStorage.getItem(key(user.id_usuarios)):null);
 useEffect(()=>{if(user)setSrc(localStorage.getItem(key(user.id_usuarios)))},[user]);
 function choose(event:ChangeEvent<HTMLInputElement>){const file=event.target.files?.[0];if(!file||!user)return;if(file.size>2*1024*1024){alert('Escolha uma imagem de até 2 MB.');return}const reader=new FileReader();reader.onload=()=>{const value=String(reader.result);localStorage.setItem(key(user.id_usuarios),value);setSrc(value);window.dispatchEvent(new CustomEvent('avatar:changed',{detail:value}))};reader.readAsDataURL(file)}
 useEffect(()=>{const changed=(event:Event)=>setSrc((event as CustomEvent<string>).detail);window.addEventListener('avatar:changed',changed);return()=>window.removeEventListener('avatar:changed',changed)},[]);
 const picture=<span className="user-avatar__picture">{src?<img src={src} alt={`Foto de ${user?.nome||'usuário'}`}/>:<UserRound/>}</span>;
 if(!editable)return <span className="user-avatar">{picture}</span>;
 return <label className="user-avatar user-avatar--editable">{picture}<span className="user-avatar__camera"><Camera/></span><span className="user-avatar__text">Alterar foto</span><input type="file" accept="image/png,image/jpeg,image/webp" onChange={choose}/></label>
}
