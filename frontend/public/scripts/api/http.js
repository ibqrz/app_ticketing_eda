import { config } from "../config.js";

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
  let response;
  try {
    response = await fetch(config.apiUrl + path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error("Sem conexão com a API. Verifique se os serviços estão em execução.");
  }
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(message(body?.detail));
  }
  return body;
}
