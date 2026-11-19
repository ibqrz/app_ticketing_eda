import { cover } from "./cover.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";
import { dayNumber, money, monthShort, until, when } from "./format.js";

function meta(name, text) {
  return h("p", { class: "card-meta" }, icon(name, 16), h("span", {}, text));
}

export function ticketCard(ticket, onBuy) {
  const lowest = Math.min(...ticket.types.map((type) => type.price));
  const label = ticket.sold_out ? "Esgotado" : "Comprar";
  return h(
    "article",
    { class: `card ticket-card${ticket.sold_out ? " is-soldout" : ""}` },
    h(
      "div",
      { class: "cover-wrap" },
      cover(ticket.id, ticket.image),
      h(
        "div",
        { class: "date-badge" },
        h("strong", {}, dayNumber(ticket.dt_event)),
        h("span", {}, monthShort(ticket.dt_event)),
      ),
    ),
    ticket.sold_out ? h("div", { class: "ribbon" }, "Esgotado") : null,
    h(
      "div",
      { class: "card-body" },
      h("h3", { class: "card-title" }, ticket.name),
      meta("calendar", `${when(ticket.dt_event)}, vendas até ${until(ticket.sales_end)}`),
      meta("pin", ticket.location),
      meta("building", `Organizado por ${ticket.organizer}`),
      h("p", { class: "card-text" }, ticket.description),
      h(
        "p",
        { class: "card-stock" },
        ticket.sold_out ? "Ingressos esgotados" : `${ticket.available} ingressos disponíveis`,
      ),
      h(
        "div",
        { class: "card-foot" },
        h("div", {}, h("small", {}, "A partir de"), h("span", { class: "price" }, money(lowest))),
        h(
          "button",
          {
            type: "button",
            class: "button primary small",
            disabled: ticket.sold_out || !ticket.open,
            onclick: () => onBuy(ticket),
          },
          label,
        ),
      ),
    ),
  );
}
