import { ArrowLeft, Pencil, Trash2 } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Feedback } from '../components/Feedback';
import { MateriaForm } from '../components/MateriaForm';
import { api, ApiError } from '../services/api';
import type { Materia } from '../types/api';
import './MateriasPage.css';

interface Entrega {
  id_entregas: number;
  titulo: string;
  data_vencimento: string;
  situacao: 'pendente' | 'realizado';
}

type Consulta<T> =
  | { status: 'carregando' }
  | { status: 'erro'; mensagem: string }
  | { status: 'pronto'; dados: T };

export function MateriaDetalhePage() {
  const { idMateria = '' } = useParams();
  const id = Number(idMateria);
  const idValido = /^\d+$/.test(idMateria) && id > 0 && id <= 2147483647;

  return (
    <div className="materias-page">
      <Link className="back-link materias-page__back" to="/materias">
        <ArrowLeft size={18} aria-hidden="true" />
        Voltar para Matérias
      </Link>
      {idValido ? <MateriaDetalhe key={id} id={id} /> : <Feedback>Matéria não encontrada.</Feedback>}
    </div>
  );
}

function MateriaDetalhe({ id }: { id: number }) {
  const navigate = useNavigate();
  const url = `/api/materias/${id}`;
  const requisicoes = useRef<AbortController | null>(null);
  const [materia, setMateria] = useState<Consulta<Materia>>({ status: 'carregando' });
  const [entregas, setEntregas] = useState<Consulta<Entrega[]>>({ status: 'carregando' });
  const [editando, setEditando] = useState(false);
  const [excluindo, setExcluindo] = useState(false);
  const [erroExclusao, setErroExclusao] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    const { signal } = controller;
    requisicoes.current = controller;

    void api<Materia>(url, { signal }).then(
      (dados) => {
        if (!signal.aborted) setMateria({ status: 'pronto', dados });
      },
      (erro: unknown) => {
        if (signal.aborted) return;

        if (erro instanceof ApiError && erro.status === 404) {
          setMateria({ status: 'erro', mensagem: 'Matéria não encontrada.' });
        } else {
          const mensagem = erro instanceof Error ? erro.message : 'Não foi possível carregar a matéria.';
          setMateria({ status: 'erro', mensagem });
        }
      },
    );

    void api<Entrega[]>(`${url}/entregas`, { signal }).then(
      (dados) => {
        if (!signal.aborted) setEntregas({ status: 'pronto', dados });
      },
      (erro: unknown) => {
        if (signal.aborted) return;
        const mensagem = erro instanceof Error ? `Falha ao carregar as entregas. ${erro.message}` : 'Falha ao carregar as entregas.';
        setEntregas({ status: 'erro', mensagem });
      },
    );

    return () => controller.abort();
  }, [url]);

  async function atualizar(dados: Pick<Materia, 'nome' | 'descricao'>) {
    const atualizada = await api<Materia>(url, {
      method: 'PUT',
      body: JSON.stringify(dados),
      signal: requisicoes.current?.signal,
    });
    setMateria({ status: 'pronto', dados: atualizada });
    setEditando(false);
  }

  async function excluir() {
    if (excluindo || materia.status !== 'pronto') return;
    const confirmou = window.confirm(
      `Excluir a matéria “${materia.dados.nome}”? As entregas, anotações e sessões Pomodoro vinculadas também serão removidas.`,
    );
    if (!confirmou) return;

    const signal = requisicoes.current?.signal;
    setExcluindo(true);
    setErroExclusao('');
    try {
      await api(url, { method: 'DELETE', signal });
      if (!signal?.aborted) navigate('/materias', { replace: true });
    } catch (erro) {
      if (signal?.aborted) return;
      setErroExclusao(erro instanceof Error ? erro.message : 'Não foi possível excluir a matéria.');
      setExcluindo(false);
    }
  }

  if (materia.status === 'carregando') return <p role="status">Carregando matéria...</p>;
  if (materia.status === 'erro') return <Feedback>{materia.mensagem}</Feedback>;

  return (
    <>
      <section className="materias-page__item materias-page__details" aria-labelledby="materia-titulo">
        <div>
          <h2 id="materia-titulo">{materia.dados.nome}</h2>
          <p>{materia.dados.descricao || 'Sem descrição.'}</p>
        </div>
        {erroExclusao && <Feedback>{erroExclusao}</Feedback>}
        {!editando && (
          <div className="materias-page__actions">
            <button className="btn secondary" type="button" disabled={excluindo} onClick={() => setEditando(true)}>
              <Pencil size={18} aria-hidden="true" />
              Editar matéria
            </button>
            <button className="btn danger" type="button" disabled={excluindo} onClick={excluir}>
              <Trash2 size={18} aria-hidden="true" />
              {excluindo ? 'Excluindo...' : 'Excluir matéria'}
            </button>
          </div>
        )}
      </section>

      {editando && (
        <MateriaForm
          titulo="Editar matéria"
          materia={materia.dados}
          onSave={atualizar}
          onCancel={() => setEditando(false)}
        />
      )}

      <section className="materias-page__item materias-page__details" aria-labelledby="materia-entregas">
        <h2 id="materia-entregas">Entregas vinculadas</h2>
        {entregas.status === 'carregando' && <p role="status">Carregando entregas...</p>}
        {entregas.status === 'erro' && <Feedback>{entregas.mensagem}</Feedback>}
        {entregas.status === 'pronto' && (
          entregas.dados.length === 0 ? <p>Nenhuma entrega vinculada.</p> : (
            <ul className="materias-page__deliveries">
              {entregas.dados.map((entrega) => (
                <li key={entrega.id_entregas}>
                  <h3>{entrega.titulo}</h3>
                  <p>
                    Vencimento em{' '}
                    <time dateTime={entrega.data_vencimento}>{entrega.data_vencimento.split('-').reverse().join('/')}</time>
                    {' · '}{entrega.situacao === 'realizado' ? 'Realizada' : 'Pendente'}
                  </p>
                </li>
              ))}
            </ul>
          )
        )}
      </section>
    </>
  );
}
