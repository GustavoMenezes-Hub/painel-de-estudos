import { BookMarked, CalendarDays, Check, FileText, Plus, Timer } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { Feedback } from '../components/Feedback';
import { api } from '../services/api';
import { concluirEntrega } from '../services/entregas';
import type { Entrega, Materia } from '../types/api';
import { compararVencimentos, dataLocal, formatarVencimento, rotuloEntrega } from '../utils/entregas';
import './PainelPage.css';

export function PainelPage() {
  const requisicoes = useRef<AbortController | null>(null);
  const [materias, setMaterias] = useState<Materia[] | null>(null);
  const [entregas, setEntregas] = useState<Entrega[] | null>(null);
  const [erroMaterias, setErroMaterias] = useState('');
  const [erroEntregas, setErroEntregas] = useState('');
  const [erroConclusao, setErroConclusao] = useState('');
  const [concluindo, setConcluindo] = useState<number | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const { signal } = controller;
    requisicoes.current = controller;

    void api<Materia[]>('/api/materias', { signal }).then(
      (lista) => { if (!signal.aborted) setMaterias(lista); },
      (erro: unknown) => {
        if (!signal.aborted) {
          const mensagem = erro instanceof Error ? ` ${erro.message}` : '';
          setErroMaterias(`Falha ao carregar as matérias.${mensagem}`);
        }
      },
    );
    void api<Entrega[]>('/api/entregas', { signal }).then(
      (lista) => { if (!signal.aborted) setEntregas(lista); },
      (erro: unknown) => {
        if (!signal.aborted) {
          const mensagem = erro instanceof Error ? ` ${erro.message}` : '';
          setErroEntregas(`Falha ao carregar as entregas.${mensagem}`);
        }
      },
    );

    return () => controller.abort();
  }, []);

  const pendentes = entregas?.filter((entrega) => entrega.situacao === 'pendente').sort(compararVencimentos);
  const nomes = new Map(materias?.map((materia) => [materia.id_materias, materia.nome]));
  const hoje = dataLocal();

  async function concluir(id: number) {
    if (concluindo !== null) return;
    const signal = requisicoes.current?.signal;
    setConcluindo(id);
    setErroConclusao('');
    try {
      const atualizada = await concluirEntrega(id, signal);
      if (!signal?.aborted) {
        setEntregas((lista) => lista?.map((entrega) => entrega.id_entregas === id ? atualizada : entrega) ?? null);
      }
    } catch (erro) {
      if (!signal?.aborted) {
        const mensagem = erro instanceof Error ? ` ${erro.message}` : '';
        setErroConclusao(`Falha ao concluir a entrega.${mensagem}`);
      }
    } finally {
      if (!signal?.aborted) setConcluindo(null);
    }
  }

  return (
    <div className="painel-page">
      <dl className="painel-page__totais" aria-label="Totais" aria-live="polite">
        <div>
          <dt><BookMarked size={20} aria-hidden="true" /> Matérias cadastradas</dt>
          <dd>{materias?.length ?? (erroMaterias ? 'Indisponível' : 'Carregando…')}</dd>
        </div>
        <div>
          <dt><CalendarDays size={20} aria-hidden="true" /> Entregas em aberto</dt>
          <dd>{pendentes?.length ?? (erroEntregas ? 'Indisponível' : 'Carregando…')}</dd>
        </div>
      </dl>

      {erroMaterias && <Feedback>{erroMaterias}</Feedback>}
      {materias?.length === 0 && <p>Use <strong>Nova matéria</strong> para cadastrar sua primeira matéria e organizar suas entregas.</p>}

      <nav className="painel-page__atalhos" aria-label="Atalhos do painel">
        <Link className="btn primary" to="/materias?nova=1"><Plus size={18} aria-hidden="true" /> Nova matéria</Link>
        <Link className="btn primary" to="/entregas?nova=1"><Plus size={18} aria-hidden="true" /> Nova entrega</Link>
        <Link className="btn secondary" to="/anotacoes"><FileText size={18} aria-hidden="true" /> Anotações</Link>
        <Link className="btn secondary" to="/pomodoro"><Timer size={18} aria-hidden="true" /> Pomodoro</Link>
      </nav>

      <section className="painel-page__pendencias" aria-labelledby="painel-entregas">
        <h2 id="painel-entregas">Entregas pendentes</h2>
        {erroEntregas && <Feedback>{erroEntregas}</Feedback>}
        {erroConclusao && <Feedback>{erroConclusao}</Feedback>}
        {pendentes?.length === 0 && <p>Nenhuma entrega em aberto.</p>}
        {pendentes && pendentes.length > 0 && (
          <ul className="painel-page__lista">
            {pendentes.map((entrega) => (
              <li key={entrega.id_entregas}>
                <div>
                  <h3>{entrega.titulo}</h3>
                  <p>{nomes.get(entrega.id_materias) ?? `Matéria #${entrega.id_materias}`}</p>
                  <p>
                    <time dateTime={entrega.data_vencimento}>{formatarVencimento(entrega.data_vencimento)}</time>
                    {' · '}<strong>{rotuloEntrega(entrega, hoje)}</strong>
                  </p>
                </div>
                <button
                  className="btn secondary"
                  type="button"
                  disabled={concluindo !== null}
                  onClick={() => void concluir(entrega.id_entregas)}
                >
                  <Check size={18} aria-hidden="true" />
                  {concluindo === entrega.id_entregas ? 'Concluindo…' : 'Marcar como concluída'}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
