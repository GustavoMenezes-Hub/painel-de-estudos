import { BookMarked, Plus } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Feedback } from '../components/Feedback';
import { MateriaForm } from '../components/MateriaForm';
import { api } from '../services/api';
import type { Materia } from '../types/api';
import './MateriasPage.css';

export function MateriasPage() {
  const [materias, setMaterias] = useState<Materia[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erroLista, setErroLista] = useState('');
  const [formularioAberto, setFormularioAberto] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    async function carregarMaterias() {
      try {
        const lista = await api<Materia[]>('/api/materias', { signal: controller.signal });
        if (!controller.signal.aborted) setMaterias(lista);
      } catch (erro) {
        if (!controller.signal.aborted) {
          setErroLista(erro instanceof Error ? erro.message : 'Não foi possível carregar as matérias.');
        }
      } finally {
        if (!controller.signal.aborted) setCarregando(false);
      }
    }

    void carregarMaterias();
    return () => controller.abort();
  }, []);

  async function cadastrar(dados: Pick<Materia, 'nome' | 'descricao'>) {
    const materia = await api<Materia>('/api/materias', {
      method: 'POST',
      body: JSON.stringify(dados),
    });
    setMaterias((lista) => [...lista, materia]);
    setFormularioAberto(false);
  }

  return (
    <div className="materias-page">
      <button
        className="btn primary fit"
        type="button"
        disabled={carregando || formularioAberto}
        onClick={() => setFormularioAberto(true)}
      >
        <Plus size={18} aria-hidden="true" />
        Nova matéria
      </button>

      {formularioAberto && (
        <MateriaForm titulo="Nova matéria" onSave={cadastrar} onCancel={() => setFormularioAberto(false)} />
      )}

      {carregando && <p role="status">Carregando matérias...</p>}
      {erroLista && <Feedback>{erroLista}</Feedback>}
      {!carregando && !erroLista && materias.length === 0 && (
        <div className="empty-state">
          <span><BookMarked aria-hidden="true" /></span>
          <h2>Nenhuma matéria cadastrada</h2>
        </div>
      )}
      {materias.length > 0 && (
        <ul className="materias-page__list" aria-label="Matérias cadastradas">
          {materias.map((materia) => (
            <li key={materia.id_materias} className="materias-page__item">
              <h2>{materia.nome}</h2>
              {materia.descricao && <p>{materia.descricao}</p>}
              <Link className="btn secondary materias-page__detail-link" to={`/materias/${materia.id_materias}`}>
                Ver detalhes
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
