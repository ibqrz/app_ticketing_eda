const currency = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

const dayFormat = new Intl.DateTimeFormat("pt-BR", {
  weekday: "long",
  day: "numeric",
  month: "long",
  hour: "2-digit",
  minute: "2-digit",
  timeZone: "America/Sao_Paulo",
});

const timeFormat = new Intl.DateTimeFormat("pt-BR", {
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  timeZone: "America/Sao_Paulo",
});

const STATUS = {
  PROCESSING: "Em processamento",
  CONFIRMED: "Confirmado",
  REFUSED: "Recusado",
};

const REASON = {
  LIMIT_EXCEEDED: "Valor acima do limite permitido",
  SOLD_OUT: "Ingressos esgotados",
};

export const money = (value) => currency.format(Number(value));

export const day = (iso) => dayFormat.format(new Date(iso));

export const time = (iso) => timeFormat.format(new Date(iso));

export const statusLabel = (status) => STATUS[status] ?? status;

export const reasonLabel = (reason) => REASON[reason] ?? "Pagamento não concluído";
