import { getOrder, refundTicket } from "../api/orders.js";
import { config } from "../config.js";
import { cover } from "./cover.js";
import { orderInfo } from "./detail.js";
import { find, h } from "./dom.js";
import { money } from "./format.js";
import { icon } from "./icons.js";
import { statePill } from "./orderRow.js";
import { toast } from "./toast.js";

const nodes = {
  dialog: find("#order-dialog"),
  scroll: find("#order-dialog .checkout-scroll"),
  banner: find("#order-banner"),
  info: find("#order-info"),
  status: find("#order-status"),
  units: find("#order-units"),
  close: find("#order-close"),
};

let current = null;
let busy = false;
let timer = null;
let confirming = null;
let changed = () => {};

function stop() {
  clearTimeout(timer);
  timer = null;
  busy = false;
  confirming = null;
}

function say(text) {
  nodes.status.textContent = text ?? "";
  nodes.status.hidden = !text;
}

function choose(index) {
  confirming = index;
  render();
}

function action(index, refunded) {
  if (refunded) {
    return h("span", { class: "pill inactive" }, "Reembolsado");
  }
  if (!current.active) {
    return h("span", { class: "pill inactive" }, "Evento realizado");
  }
  if (confirming === index) {
    return h(
      "div",
      { class: "unit-confirm" },
      h("button", { type: "button", class: "button small danger fill", onclick: request }, "Confirmar"),
      h("button", { type: "button", class: "button small", onclick: () => choose(null) }, "Cancelar"),
    );
  }
  return h(
    "button",
    { type: "button", class: "button small danger", disabled: busy, onclick: () => choose(index) },
    "Reembolsar",
  );
}

function unit(index) {
  const refunded = index < current.refunded;
  const price = money(Number(current.total) / current.quantity);
  return h(
    "li",
    { class: `unit${refunded ? " is-refunded" : ""}` },
    icon("ticket", 20),
    h(
      "div",
      { class: "unit-label" },
      h("strong", {}, `Ingresso ${index + 1}`),
      h("small", {}, `${current.ticket_type} · ${price}`),
    ),
    action(index, refunded),
  );
}

function render() {
  nodes.info.querySelector(".order-head .pill")?.replaceWith(statePill(current));
  nodes.units.replaceChildren(...Array.from({ length: current.quantity }, (_, index) => unit(index)));
}

function finish(order, text) {
  current = order;
  busy = false;
  say(text);
  render();
  changed();
}

function poll(before, attempt = 0) {
  timer = setTimeout(async () => {
    const order = await getOrder(current.id).catch(() => null);
    if (order && order.refunded > before) {
      finish(order, null);
      toast("Ingresso reembolsado com sucesso.");
      return;
    }
    if (attempt + 1 >= config.pollMax) {
      finish(current, "O reembolso ainda está sendo processado. Ele aparecerá aqui em instantes.");
      return;
    }
    poll(before, attempt + 1);
  }, config.pollMs);
}

async function request() {
  confirming = null;
  busy = true;
  render();
  try {
    await refundTicket(current.id);
    if (!nodes.dialog.open) {
      return;
    }
    say("Reembolso solicitado. Processando…");
    poll(current.refunded);
  } catch (error) {
    busy = false;
    render();
    toast(error.message);
  }
}

export function openOrder(order, onChange) {
  stop();
  current = order;
  changed = onChange;
  nodes.banner.replaceChildren(cover(order.image, "banner"));
  nodes.info.replaceChildren(...orderInfo(order));
  say(null);
  render();
  nodes.scroll.scrollTop = 0;
  nodes.dialog.showModal();
}

nodes.close.addEventListener("click", () => nodes.dialog.close());
nodes.dialog.addEventListener("close", stop);
nodes.dialog.addEventListener("click", (event) => {
  if (event.target === nodes.dialog) {
    nodes.dialog.close();
  }
});