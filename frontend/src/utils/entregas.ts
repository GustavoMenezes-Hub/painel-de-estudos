import type { Entrega } from '../types/api';

export function dataLocal(data = new Date()): string {
  const ano = String(data.getFullYear()).padStart(4, '0');
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const dia = String(data.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

export function formatarVencimento(data: string): string {
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano}`;
}

export function rotuloEntrega(entrega: Entrega, hoje: string): string {
  if (entrega.situacao === 'realizado') return 'Concluída';
  if (entrega.data_vencimento < hoje) return 'Atrasada';
  if (entrega.data_vencimento === hoje) return 'Vence hoje';
  return 'Próxima';
}

export function compararVencimentos(a: Entrega, b: Entrega): number {
  return a.data_vencimento.localeCompare(b.data_vencimento) || a.id_entregas - b.id_entregas;
}
