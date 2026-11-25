import { Navigate,Outlet,useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
export function ProtectedRoute(){const {user,checking}=useAuth();const location=useLocation();if(checking)return <div className="page-loader"><span className="spinner"/>Verificando sua sessão...</div>;return user?<Outlet/>:<Navigate to="/entrar" replace state={{from:location}}/>}
