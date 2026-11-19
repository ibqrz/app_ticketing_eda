import { listOrders } from "../api/orders.js";
import { listTickets } from "../api/tickets.js";
import { config } from "../config.js";
import { goLogin, isLogged } from "../state/session.js";
import { mountCarousel } from "../ui/carousel.js";
import { openCheckout } from "../ui/checkout.js";
import { empty, find, h } from "../ui/dom.js";
import { renderLayout } from "../ui/layout.js";
import { orderRow } from "../ui/orderRow.js";
import { ticketCard } from "../ui/ticketCard.js";
import { toast } from "../ui/toast.js";

renderLayout("home");

const events = find("#events");
const list = find("#orders-list");
const more = find("#orders-more");

function buy(ticket) {
  if (!isLogged()) {
    goLogin();
    return;
  }
  openCheckout(ticket, refresh);
}

async function loadTickets(quiet = false) {
  try {
    const tickets = await listTickets();
    if (tickets.length === 0) {
      events.replaceChildren(empty("Nenhum evento encontrado"));
      return;
    }
    mountCarousel(events, tickets.map((ticket) => ticketCard(ticket, buy)));
  } catch (error) {
    if (!quiet) {
      toast(error.message);
      events.replaceChildren(empty("Não foi possível carregar os eventos"));
    }
  }
}

function guest() {
  return h(
    "div",
    { class: "guest" },
    empty("Entre na sua conta para ver seus ingressos"),
    h("a", { class: "button primary", href: "login.html" }, "Entrar"),
  );
}

async function loadOrders(quiet = false) {
  if (!isLogged()) {
    list.replaceChildren(guest());
    more.hidden = true;
    return;
  }
  try {
    const orders = await listOrders("purchased", config.homeOrders + 1);
    if (orders.length === 0) {
      list.replaceChildren(empty("Nenhum ingresso comprado"));
    } else {
      list.replaceChildren(...orders.slice(0, config.homeOrders).map(orderRow));
    }
    more.hidden = orders.length <= config.homeOrders;
  } catch (error) {
    if (!quiet) {
      toast(error.message);
    }
  }
}

function refresh() {
  loadTickets();
  loadOrders();
}

refresh();
setInterval(() => loadOrders(true), config.refreshMs);
setInterval(() => loadTickets(true), config.ticketsMs);
