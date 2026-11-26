import { Navigate, Route, Routes } from 'react-router-dom';
import { EntregasSection } from './components/EntregasSection';
import { AppLayout } from './layouts/AppLayout';
import { LoginPage } from './pages/LoginPage';
import { MateriaDetalhePage } from './pages/MateriaDetalhePage';
import { MateriasPage } from './pages/MateriasPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { ProfilePage } from './pages/ProfilePage';
import { RegisterPage } from './pages/RegisterPage';
import { WelcomePage } from './pages/WelcomePage';
import { ProtectedRoute } from './routes/ProtectedRoute';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/entrar" element={<LoginPage />} />
      <Route path="/cadastro" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/materias" element={<MateriasPage />} />
          <Route path="/materias/:idMateria" element={<MateriaDetalhePage />} />
          <Route path="/entregas" element={<EntregasSection />} />

          {['painel', 'anotacoes', 'pomodoro'].map((page) => (
            <Route
              key={page}
              path={`/${page}`}
              element={<PlaceholderPage />}
            />
          ))}

          <Route path="/perfil" element={<ProfilePage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
