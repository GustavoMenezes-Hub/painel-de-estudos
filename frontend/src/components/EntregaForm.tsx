import { useId, useState, type FormEvent } from 'react';
import type { DadosEntrega, Entrega, Materia } from '../types/api';
import { Feedback } from './Feedback';
import { FormField } from './FormField';

interface EntregaFormProps {
  materias: Materia[];
  materiaInicial?: number;
  entrega?: Entrega;
  disabled?: boolean;
  onSave: (dados: DadosEntrega) => Promise<void>;
  onCancel: () => void;
}

export function EntregaForm({ materias, materiaInicial, entrega, disabled, onSave, onCancel }: EntregaFormProps) {
  const id = useId();
  const [titulo, setTitulo] = useState(entrega?.titulo ?? '');
  const [materia, setMateria] = useState(String(entrega?.id_materias ?? materiaInicial ?? ''));
  const [vencimento, setVencimento] = useState(entrega?.data_vencimento ?? '');
  const [situacao, setSituacao] = useState<DadosEntrega['situacao']>(entrega?.situacao ?? 'pendente');
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState('');
  const bloqueado = disabled || salvando;
  const materiaSelecionada = materias.some((item) => String(item.id_materias) === materia) ? materia : '';

  async function salvar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (bloqueado) return;

    const tituloLimpo = titulo.trim();
    if (!tituloLimpo) {
      setErro('Informe o título da entrega.');
      return;
    }

    setSalvando(true);
    setErro('');
    try {
      await onSave({
        titulo: tituloLimpo,
        id_materias: Number(materiaSelecionada),
        data_vencimento: vencimento,
        situacao,
      });
    } catch (falha) {
      setErro(falha instanceof Error ? falha.message : 'Não foi possível salvar a entrega.');
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form className="entregas-section__form" aria-label={entrega ? 'Editar entrega' : 'Nova entrega'} onSubmit={salvar}>
      {erro && <Feedback>{erro}</Feedback>}
      <FormField
        id={`${id}-titulo`}
        label="Título"
        value={titulo}
        onChange={(event) => setTitulo(event.target.value)}
        required
        maxLength={100}
        disabled={bloqueado}
        autoFocus
      />
      <div className="field">
        <label htmlFor={`${id}-materia`}>Matéria</label>
        <select id={`${id}-materia`} value={materiaSelecionada} onChange={(event) => setMateria(event.target.value)} required disabled={bloqueado}>
          <option value="" disabled>Selecione uma matéria</option>
          {materias.map((item) => <option key={item.id_materias} value={item.id_materias}>{item.nome}</option>)}
        </select>
      </div>
      <FormField
        id={`${id}-vencimento`}
        label="Vencimento"
        type="date"
        value={vencimento}
        onChange={(event) => setVencimento(event.target.value)}
        min="0001-01-01"
        max="9999-12-31"
        required
        disabled={bloqueado}
      />
      <div className="field">
        <label htmlFor={`${id}-situacao`}>Situação</label>
        <select
          id={`${id}-situacao`}
          value={situacao}
          onChange={(event) => setSituacao(event.target.value === 'realizado' ? 'realizado' : 'pendente')}
          disabled={bloqueado}
        >
          <option value="pendente">Pendente</option>
          <option value="realizado">Concluída</option>
        </select>
      </div>
      <div className="entregas-section__actions">
        <button className="btn primary" type="submit" disabled={bloqueado}>{salvando ? 'Salvando...' : 'Salvar entrega'}</button>
        <button className="btn secondary" type="button" onClick={onCancel} disabled={salvando}>Cancelar</button>
      </div>
    </form>
  );
}
