import { cover } from "./cover.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";
import { countText, isLive, money, paid, remaining, when } from "./format.js";

export function statePill(order) {
  if (remaining(order) === 0) {
    return h("span", { class: "pill inactive" }, "Reembolsado");
  }
  return h("span", { class: `pill ${order.active ? "active" : "inactive"}` }, order.active ? "Ativo" : "Inativo");
}

export function orderRow(order, open) {
  return h(
    "article",
    { class: `card row-card${isLive(order) ? "" : " is-inactive"}` },
    cover(order.image, "thumb"),
    h(
      "div",
      { class: "row-main" },
      h(
        "h3",
        { class: "card-title" },
        h("button", { type: "button", class: "card-open", onclick: () => open(order) }, order.ticket_name),
      ),
      h("p", { class: "muted small" }, countText(order)),
      h("p", { class: "card-meta" }, icon("calendar", 16), h("span", {}, when(order.dt_event))),
    ),
    h(
      "div",
      { class: "row-side" },
      h("strong", { class: "price" }, money(paid(order))),
      statePill(order),
    ),
  );
}