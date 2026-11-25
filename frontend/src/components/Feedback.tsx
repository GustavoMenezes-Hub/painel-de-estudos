import { AlertCircle,CheckCircle2 } from 'lucide-react';
export function Feedback({type='error',children}:{type?:'error'|'success';children:string}){return <div className={`feedback feedback--${type}`} role={type==='error'?'alert':'status'}>{type==='error'?<AlertCircle size={18}/>:<CheckCircle2 size={18}/>}<span>{children}</span></div>}
