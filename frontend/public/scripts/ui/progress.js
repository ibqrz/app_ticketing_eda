import { cover } from "./cover.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";
import { money, reasonLabel, time } from "./format.js";

export const STEPS = ["Pedido recebido", "Ingressos reservados", "Pagamento", "Confirmação"];

const ACTIONS = [
  "Registrando o pedido",
  "Reservando seus ingressos",
  "Processando o pagamento",
  "Confirmando o pedido",
];

const REACHED = { RECEIVED: 1, RESERVED: 2, PAID: 3, CONFIRMED: 4 };

export function progressOf(order) {
  if (order.status === "REFUSED") {
    const failed = order.reason === "SOLD_OUT" ? 2 : 3;
    return { refused: true, failed, done: failed - 1, percent: (failed / STEPS.length) * 100 };
  }
  const done = REACHED[order.stage] ?? 1;
  return { refused: false, failed: 0, done, percent: (done / STEPS.length) * 100 };
}

export function headline(order) {
  const progress = progressOf(order);
  if (progress.refused) {
    return `Recusado: ${reasonLabel(order.reason)}`;
  }
  if (order.status === "CONFIRMED") {
    return "Pedido confirmado";
  }
  return `Em andamento: ${ACTIONS[progress.done]}`;
}

export function stepper(order) {
  const progress = progressOf(order);
  return h(
    "ol",
    { class: "stepper" },
    STEPS.map((label, index) => {
      const number = index + 1;
      let state = "pending";
      let symbol = String(number);
      if (number <= progress.done) {
        state = "done";
        symbol = icon("check", 15);
      } else if (progress.refused && number === progress.failed) {
        state = "failed";
        symbol = icon("close", 15);
      } else if (!progress.refused && number === progress.done + 1) {
        state = "current";
      }
      return h(
        "li",
        { class: `step ${state}` },
        h("span", { class: "dot" }, symbol),
        h("span", {}, label),
      );
    }),
  );
}

export function progressCard(order) {
  const progress = progressOf(order);
  const instance = order.processed_by ? `, pagamento na instância ${order.processed_by}` : "";
  return h(
    "article",
    { class: `card progress-card${progress.refused ? " is-failed" : ""}` },
    h(
      "div",
      { class: "progress-head" },
      cover(order.image, "thumb"),
      h(
        "div",
        {},
        h("h3", { class: "card-title" }, order.ticket_name),
        h("p", { class: "muted small" }, `${order.quantity} x ${order.ticket_type}, ${money(order.total)}`),
      ),
    ),
    h(
      "div",
      {
        class: "bar",
        role: "progressbar",
        "aria-valuemin": 0,
        "aria-valuemax": 100,
        "aria-valuenow": Math.round(progress.percent),
        "aria-label": "Andamento do pedido",
      },
      h("span", { class: "fill", style: `width:${progress.percent}%` }),
    ),
    h("p", { class: "progress-status" }, headline(order)),
    stepper(order),
    h(
      "p",
      { class: "muted small" },
      `Pedido ${order.id.slice(0, 8)}, criado às ${time(order.created_at)}${instance}`,
    ),
  );
}
