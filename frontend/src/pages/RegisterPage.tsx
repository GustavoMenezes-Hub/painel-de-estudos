import { useState,type FormEvent,type ChangeEvent } from 'react';
import { Link,useNavigate } from 'react-router-dom';
import { ArrowLeft,ArrowRight } from 'lucide-react';
import { Brand } from '../components/Brand';
import { FormField } from '../components/FormField';
import { Feedback } from '../components/Feedback';
import { api } from '../services/api';

export function RegisterPage(){
 const [form,setForm]=useState({nome:'',email:'',senha:''}); const [error,setError]=useState(''); const [busy,setBusy]=useState(false); const nav=useNavigate();
 const change=(key:keyof typeof form)=>(e:ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:e.target.value});
 async function submit(e:FormEvent){e.preventDefault();setError('');if(!form.nome.trim()||!form.email.trim()){setError('Preencha seu nome e seu e-mail.');return}if(form.senha.length<8||form.senha.length>128){setError('A senha precisa ter entre 8 e 128 caracteres.');return}setBusy(true);try{await api('/api/usuarios',{method:'POST',body:JSON.stringify(form)});nav('/entrar',{replace:true,state:{success:'Conta criada com sucesso. Agora, entre com seus dados.'}})}catch(e){setError(e instanceof Error?e.message:'Não foi possível criar sua conta.')}finally{setBusy(false)}}
 return <div className="auth-page register-page"><main className="auth-form-area"><form className="auth-card" onSubmit={submit} noValidate><Brand light/>{error&&<Feedback>{error}</Feedback>}<FormField id="nome" label="Nome" placeholder="Nome" autoComplete="name" value={form.nome} onChange={change('nome')}/><FormField id="email" label="E-mail" type="email" placeholder="E-mail" autoComplete="email" value={form.email} onChange={change('email')}/><FormField id="senha" label="Senha" type="password" placeholder="Senha" autoComplete="new-password" hint="A senha deve ter de 8 a 128 caracteres." value={form.senha} onChange={change('senha')}/><button className="btn primary" disabled={busy}>{busy?<><span className="spinner small"/>Criando...</>:<>Criar<ArrowRight size={19}/></>}</button><Link className="auth-back-home" to="/entrar"><ArrowLeft size={16}/>Voltar para entrar</Link></form></main><section className="register-photo" aria-label="Estudante lendo um caderno"/></div>
}
