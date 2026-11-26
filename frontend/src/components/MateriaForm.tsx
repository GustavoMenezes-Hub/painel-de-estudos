import { useState, type FormEvent } from 'react';
import type { Materia } from '../types/api';
import { Feedback } from './Feedback';
import { FormField } from './FormField';

type DadosMateria = Pick<Materia, 'nome' | 'descricao'>;

interface MateriaFormProps {
  titulo: string;
  materia?: Materia;
  onSave: (dados: DadosMateria) => Promise<void>;
  onCancel: () => void;
}

export function MateriaForm({ titulo, materia, onSave, onCancel }: MateriaFormProps) {
  const [nome, setNome] = useState(materia?.nome ?? '');
  const [descricao, setDescricao] = useState(materia?.descricao ?? '');
  const [salvando, setSalvando] = useState(false);
  const [erroFormulario, setErroFormulario] = useState('');

  async function salvar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (salvando) return;

    const nomeLimpo = nome.trim();
    if (!nomeLimpo) {
      setErroFormulario('Informe o nome da matéria.');
      return;
    }

    setSalvando(true);
    setErroFormulario('');
    try {
      await onSave({ nome: nomeLimpo, descricao: descricao.trim() || null });
    } catch (erro) {
      setErroFormulario(erro instanceof Error ? erro.message : 'Não foi possível salvar a matéria.');
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form className="materias-page__form" aria-label={titulo} onSubmit={salvar}>
      {erroFormulario && <Feedback>{erroFormulario}</Feedback>}
      <FormField
        id="materia-nome"
        label="Nome"
        value={nome}
        onChange={(event) => setNome(event.target.value)}
        required
        maxLength={100}
        disabled={salvando}
        autoFocus
      />
      <div className="field">
        <label htmlFor="materia-descricao">Descrição (opcional)</label>
        <textarea
          id="materia-descricao"
          value={descricao}
          onChange={(event) => setDescricao(event.target.value)}
          rows={3}
          maxLength={2000}
          disabled={salvando}
        />
      </div>
      <div className="materias-page__actions">
        <button className="btn primary" type="submit" disabled={salvando}>
          {salvando ? 'Salvando...' : 'Salvar matéria'}
        </button>
        <button className="btn secondary" type="button" onClick={onCancel} disabled={salvando}>
          Cancelar
        </button>
      </div>
    </form>
  );
}
