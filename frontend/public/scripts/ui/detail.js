import { h } from "./dom.js";
import { until, when } from "./format.js";
import { icon } from "./icons.js";

function item(name, label, text) {
  return h(
    "li",
    { class: "info-item" },
    icon(name, 18),
    h("div", {}, h("small", {}, label), h("strong", {}, text)),
  );
}

function stock(ticket) {
  return ticket.sold_out ? "Esgotado" : `${ticket.available} ingressos disponíveis`;
}

export function detail(ticket) {
  return [
    h("h2", { id: "checkout-title" }, ticket.name),
    h(
      "div",
      { class: "checkout-details" },
      h(
        "ul",
        { class: "info-grid" },
        item("calendar", "Data do evento", when(ticket.dt_event)),
        item("clock", "Vendas até", until(ticket.sales_end)),
        item("pin", "Local", ticket.location),
        item("building", "Organizador", ticket.organizer),
        item("ticket", "Disponibilidade", stock(ticket)),
      ),
      h("p", { class: "checkout-text" }, ticket.description),
    ),
  ];
}
