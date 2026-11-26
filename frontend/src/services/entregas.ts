import type { Entrega } from '../types/api';
import { api } from './api';

export function concluirEntrega(id: number, signal?: AbortSignal): Promise<Entrega> {
  return api<Entrega>(`/api/entregas/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ situacao: 'realizado' }),
    signal,
  });
}
