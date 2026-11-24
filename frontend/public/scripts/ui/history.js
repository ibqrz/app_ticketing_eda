import { h } from "./dom.js";
import { money, reasonLabel, statusLabel, time } from "./format.js";

function badge(order) {
  return h(
    "td",
    {},
    h("span", { class: `badge ${order.status.toLowerCase()}` }, statusLabel(order.status)),
    order.status === "REFUSED" ? h("small", {}, reasonLabel(order.reason)) : null,
  );
}

function row(order) {
  return h(
    "tr",
    {},
    h("td", {}, order.id.slice(0, 8)),
    h(
      "td",
      {},
      h("strong", {}, order.event_title),
      h("small", {}, `${order.quantity} x ${order.ticket_name}`),
    ),
    h("td", {}, money(order.total)),
    badge(order),
    h("td", {}, order.processed_by ?? "Aguardando"),
    h("td", {}, time(order.created_at)),
  );
}

export function renderOrders(body, empty, orders) {
  empty.hidden = orders.length > 0;
  body.replaceChildren(...orders.map(row));
}