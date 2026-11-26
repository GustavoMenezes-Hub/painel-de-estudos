import { CalendarDays, Check, Pencil, Plus, Trash2 } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { api } from '../services/api';
import type { DadosEntrega, Entrega, Materia } from '../types/api';
import { compararVencimentos, dataLocal, formatarVencimento, rotuloEntrega } from '../utils/entregas';
import { EntregaForm } from './EntregaForm';
import { Feedback } from './Feedback';
import './EntregasSection.css';

interface EntregasSectionProps {
  materia?: Materia;
  disabled?: boolean;
}

export function EntregasSection({ materia, disabled }: EntregasSectionProps) {
  const idMateria = materia?.id_materias;
  const url = idMateria ? `/api/materias/${idMateria}/entregas` : '/api/entregas';
  const requisicoes = useRef<AbortController | null>(null);
  const [entregas, setEntregas] = useState<Entrega[] | null>(null);
  const [materias, setMaterias] = useState<Materia[] | null>(null);
  const [erroEntregas, setErroEntregas] = useState('');
  const [erroMaterias, setErroMaterias] = useState('');
  const [formulario, setFormulario] = useState<Entrega | 'nova' | null>(null);
  const [ocupado, setOcupado] = useState(false);
  const [erroAcao, setErroAcao] = useState('');
  const [mensagem, setMensagem] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    const { signal } = controller;
    requisicoes.current = controller;

    void api<Entrega[]>(url, { signal }).then(
      (lista) => { if (!signal.aborted) setEntregas(lista); },
      (erro: unknown) => {
        if (!signal.aborted) {
          setErroEntregas(erro instanceof Error ? `Falha ao carregar as entregas. ${erro.message}` : 'Falha ao carregar as entregas.');
        }
      },
    );
    void api<Materia[]>('/api/materias', { signal }).then(
      (lista) => { if (!signal.aborted) setMaterias(lista); },
      (erro: unknown) => {
        if (!signal.aborted) {
          setErroMaterias(erro instanceof Error ? `Falha ao carregar as matérias. ${erro.message}` : 'Falha ao carregar as matérias.');
        }
      },
    );

    return () => controller.abort();
  }, [url]);

  const opcoes = materia ? [materia, ...(materias ?? []).filter((item) => item.id_materias !== idMateria)] : materias ?? [];
  const nomes = new Map(opcoes.map((item) => [item.id_materias, item.nome]));
  const bloqueado = disabled || ocupado || formulario !== null;
  const entregaEmEdicao = formulario === 'nova' ? undefined : formulario ?? undefined;
  const hoje = dataLocal();
  const TituloEntrega = materia ? 'h3' : 'h2';

  function abrirFormulario(valor: Entrega | 'nova') {
    setErroAcao('');
    setMensagem('');
    setFormulario(valor);
  }

  function atualizarLista(salva: Entrega) {
    const pertenceALista = idMateria === undefined || salva.id_materias === idMateria;
    setEntregas((lista) => {
      const outras = (lista ?? []).filter((item) => item.id_entregas !== salva.id_entregas);
      return pertenceALista ? [...outras, salva] : outras;
    });
    if (!pertenceALista) setMensagem('Entrega salva em outra matéria. Você pode encontrá-la em Entregas.');
  }

  async function salvar(dados: DadosEntrega) {
    const signal = requisicoes.current?.signal;
    const salva = await api<Entrega>(entregaEmEdicao ? `/api/entregas/${entregaEmEdicao.id_entregas}` : '/api/entregas', {
      method: entregaEmEdicao ? 'PUT' : 'POST',
      body: JSON.stringify(dados),
      signal,
    });
    if (signal?.aborted) return;
    atualizarLista(salva);
    setFormulario(null);
  }

  async function executarAcao(entrega: Entrega, acao: 'concluir' | 'excluir') {
    if (bloqueado) return;
    if (acao === 'excluir' && !window.confirm(`Excluir a entrega “${entrega.titulo}”? Esta ação é permanente.`)) return;

    const signal = requisicoes.current?.signal;
    const endpoint = `/api/entregas/${entrega.id_entregas}`;
    setOcupado(true);
    setErroAcao('');
    setMensagem('');
    try {
      if (acao === 'excluir') {
        await api(endpoint, { method: 'DELETE', signal });
        if (!signal?.aborted) setEntregas((lista) => lista?.filter((item) => item.id_entregas !== entrega.id_entregas) ?? null);
      } else {
        const salva = await api<Entrega>(endpoint, {
          method: 'PATCH',
          body: JSON.stringify({ situacao: 'realizado' }),
          signal,
        });
        if (!signal?.aborted) atualizarLista(salva);
      }
    } catch (erro) {
      if (!signal?.aborted) setErroAcao(erro instanceof Error ? erro.message : 'Não foi possível atualizar a entrega.');
    } finally {
      if (!signal?.aborted) setOcupado(false);
    }
  }

  return (
    <section className="entregas-section" aria-label={materia ? 'Entregas vinculadas' : 'Entregas'}>
      <div className="entregas-section__heading">
        {materia && <h2>Entregas vinculadas</h2>}
        <button className="btn primary fit" type="button" disabled={bloqueado || !entregas || opcoes.length === 0} onClick={() => abrirFormulario('nova')}>
          <Plus size={18} aria-hidden="true" />
          Nova entrega
        </button>
      </div>

      {erroMaterias && <Feedback>{erroMaterias}</Feedback>}
      {materias?.length === 0 && !materia && <p>Cadastre uma matéria para criar entregas.</p>}
      {erroAcao && <Feedback>{erroAcao}</Feedback>}
      {mensagem && <Feedback type="success">{mensagem}</Feedback>}
      {formulario && (
        <EntregaForm
          materias={opcoes}
          materiaInicial={idMateria}
          entrega={entregaEmEdicao}
          disabled={disabled}
          onSave={salvar}
          onCancel={() => setFormulario(null)}
        />
      )}

      {erroEntregas && <Feedback>{erroEntregas}</Feedback>}
      {!entregas && !erroEntregas && <p role="status">Carregando entregas...</p>}
      {entregas?.length === 0 && (
        <div className="empty-state">
          <span><CalendarDays aria-hidden="true" /></span>
          <h2>{materia ? 'Nenhuma entrega vinculada' : 'Nenhuma entrega cadastrada'}</h2>
        </div>
      )}
      {entregas && entregas.length > 0 && (
        <ul className="entregas-section__list">
          {[...entregas].sort(compararVencimentos).map((entrega) => (
            <li key={entrega.id_entregas}>
              <div>
                <TituloEntrega className="entregas-section__title">{entrega.titulo}</TituloEntrega>
                <p>{nomes.get(entrega.id_materias) ?? `Matéria #${entrega.id_materias}`}</p>
                <p>
                  <time dateTime={entrega.data_vencimento}>{formatarVencimento(entrega.data_vencimento)}</time>
                  {' · '}<strong>{rotuloEntrega(entrega, hoje)}</strong>
                </p>
              </div>
              <div className="entregas-section__actions">
                <button className="btn secondary" type="button" disabled={bloqueado || opcoes.length === 0} onClick={() => abrirFormulario(entrega)}>
                  <Pencil size={18} aria-hidden="true" />
                  Editar
                </button>
                {entrega.situacao === 'pendente' && (
                  <button className="btn secondary" type="button" disabled={bloqueado} onClick={() => void executarAcao(entrega, 'concluir')}>
                    <Check size={18} aria-hidden="true" />
                    Marcar como concluída
                  </button>
                )}
                <button className="btn danger" type="button" disabled={bloqueado} onClick={() => void executarAcao(entrega, 'excluir')}>
                  <Trash2 size={18} aria-hidden="true" />
                  Excluir
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
