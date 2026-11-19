import { cover } from "./cover.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";
import { money, when } from "./format.js";

export function statePill(active) {
  return h("span", { class: `pill ${active ? "active" : "inactive"}` }, active ? "Ativo" : "Inativo");
}

export function orderRow(order) {
  return h(
    "article",
    { class: `card row-card${order.active ? "" : " is-inactive"}` },
    cover(order.ticket_id, order.image, "thumb"),
    h(
      "div",
      { class: "row-main" },
      h("h3", { class: "card-title" }, order.ticket_name),
      h("p", { class: "muted small" }, `${order.quantity} x ${order.ticket_type}`),
      h("p", { class: "card-meta" }, icon("calendar", 16), h("span", {}, when(order.dt_event))),
    ),
    h(
      "div",
      { class: "row-side" },
      h("strong", { class: "price" }, money(order.total)),
      statePill(order.active),
    ),
  );
}
