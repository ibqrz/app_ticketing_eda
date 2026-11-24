import { config } from "../config.js";
import { clear, goLogin, token } from "../state/session.js";

function message(detail) {
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    return "Confira os dados informados e tente novamente.";
  }
  return "Não foi possível concluir a solicitação.";
}

export async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  const current = token();
  if (current) {
    headers.Authorization = `Bearer ${current}`;
  }
  let response;
  try {
    response = await fetch(config.apiUrl + path, { ...options, headers });
  } catch {
    throw new Error("Sem conexão com a API. Verifique se os serviços estão em execução.");
  }
  const body = response.status === 204 ? null : await response.json().catch(() => null);
  if (response.status === 401 && current) {
    clear();
    goLogin();
  }
  if (!response.ok) {
    throw new Error(message(body?.detail));
  }
  return body;
}