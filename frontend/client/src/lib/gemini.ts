import { apiFetch, apiPost } from './api';
let sessionId: string | undefined;
export async function askCropQuestion(question: string): Promise<string> {
  const data = await apiPost<{ reply: string; sessionId: string }>('/api/chat', { question, sessionId });
  sessionId = data.sessionId;
  return data.reply;
}
export async function clearConversationHistory() {
  if (sessionId) await apiFetch(`/api/chat/history/${encodeURIComponent(sessionId)}`, { method: 'DELETE' });
  sessionId = undefined;
}
