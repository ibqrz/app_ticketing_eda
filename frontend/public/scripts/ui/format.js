const zone = "America/Sao_Paulo";

const currency = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

const full = new Intl.DateTimeFormat("pt-BR", {
  weekday: "short",
  day: "numeric",
  month: "short",
  hour: "2-digit",
  minute: "2-digit",
  timeZone: zone,
});

const dayOnly = new Intl.DateTimeFormat("pt-BR", { day: "2-digit", timeZone: zone });

const monthOnly = new Intl.DateTimeFormat("pt-BR", { month: "short", timeZone: zone });

const shortDate = new Intl.DateTimeFormat("pt-BR", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  timeZone: zone,
});

const clock = new Intl.DateTimeFormat("pt-BR", {
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  timeZone: zone,
});

const REASON = {
  LIMIT_EXCEEDED: "valor acima do limite permitido",
  SOLD_OUT: "ingressos esgotados",
};

export const money = (value) => currency.format(Number(value));

export const when = (iso) => full.format(new Date(iso));

export const dayNumber = (iso) => dayOnly.format(new Date(iso));

export const monthShort = (iso) => monthOnly.format(new Date(iso)).replace(".", "");

export const until = (iso) => shortDate.format(new Date(iso));

export const time = (iso) => clock.format(new Date(iso));

export const reasonLabel = (reason) => REASON[reason] ?? "pagamento não concluído";
