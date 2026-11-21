import { cover } from "./cover.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";
import { money, when } from "./format.js";
import { statePill } from "./orderRow.js";

export function orderCard(order) {
  return h(
    "article",
    { class: `card order-card${order.active ? "" : " is-inactive"}` },
    cover(order.image, "wide"),
    h(
      "div",
      { class: "card-body" },
      h(
        "div",
        { class: "order-card-top" },
        h("h3", { class: "card-title" }, order.ticket_name),
        statePill(order.active),
      ),
      h("p", { class: "muted small" }, `${order.quantity} x ${order.ticket_type}`),
      h("p", { class: "card-meta" }, icon("calendar", 16), h("span", {}, when(order.dt_event))),
      order.location
        ? h("p", { class: "card-meta" }, icon("pin", 16), h("span", {}, order.location))
        : null,
      h(
        "div",
        { class: "card-foot" },
        h("div", {}, h("small", {}, `Pedido ${order.id.slice(0, 8)}`), h("span", { class: "price" }, money(order.total))),
      ),
    ),
  );
}
