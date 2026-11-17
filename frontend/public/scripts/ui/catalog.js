import { h } from "./dom.js";
import { day, money } from "./format.js";

function row(event, ticket, onBuy) {
  const soldOut = ticket.available === 0;
  return h(
    "li",
    { class: "stub-row" },
    h(
      "div",
      {},
      h("strong", {}, ticket.name),
      h("span", { class: "muted" }, soldOut ? "Esgotado" : `${ticket.available} disponíveis`),
    ),
    h(
      "div",
      { class: "stub-action" },
      h("span", { class: "price" }, money(ticket.price)),
      h(
        "button",
        { type: "button", class: "button small", disabled: soldOut, onclick: () => onBuy(event, ticket) },
        "Comprar",
      ),
    ),
  );
}

function card(event, onBuy) {
  return h(
    "article",
    { class: "ticket" },
    h(
      "div",
      { class: "ticket-main" },
      h("p", { class: "ticket-date" }, day(event.starts_at)),
      h("h3", {}, event.title),
      h("p", {}, event.venue),
      h("p", { class: "muted" }, event.city),
    ),
    h("ul", { class: "ticket-stub" }, event.tickets.map((ticket) => row(event, ticket, onBuy))),
  );
}

export function renderCatalog(container, events, onBuy) {
  container.replaceChildren(...events.map((event) => card(event, onBuy)));
}
