import { createOrder, getOrder } from "../api/orders.js";
import { config } from "../config.js";
import { goLogin, isLogged } from "../state/session.js";
import { cover } from "./cover.js";
import { detail } from "./detail.js";
import { find, h } from "./dom.js";
import { money, reasonLabel } from "./format.js";
import { headline, stepper } from "./progress.js";

const nodes = {
  dialog: find("#checkout"),
  form: find("#checkout-form"),
  scroll: find(".checkout-scroll"),
  banner: find("#checkout-banner"),
  info: find("#checkout-info"),
  notice: find("#checkout-notice"),
  types: find("#checkout-types"),
  total: find("#checkout-total"),
  error: find("#checkout-error"),
  submit: find("#checkout-submit"),
  close: find("#checkout-close"),
  tracker: find("#tracker"),
  pulse: find("#tracker-pulse"),
  title: find("#tracker-title"),
  detail: find("#tracker-detail"),
  stepper: find("#tracker-stepper"),
  steps: find("#tracker-steps"),
  done: find("#tracker-done"),
};

let ticket = null;
let timer = null;
let refresh = () => {};

function stop() {
  clearTimeout(timer);
}

function selected() {
  const name = new FormData(nodes.form).get("type");
  return ticket.types.find((type) => type.name === name) ?? ticket.types[0];
}

function updateTotal() {
  const quantity = Number(nodes.form.elements.quantity.value) || 0;
  nodes.total.textContent = money(selected().price * quantity);
}

function option(type, index) {
  const input = h("input", {
    type: "radio",
    name: "type",
    value: type.name,
    checked: index === 0,
  });
  input.addEventListener("change", updateTotal);
  return h("label", { class: "type-option" }, input, h("span", {}, type.name), h("strong", {}, money(type.price)));
}

function readForm() {
  return {
    ticket_id: ticket.id,
    ticket_type: selected().name,
    quantity: Number(nodes.form.elements.quantity.value),
  };
}

function renderSteps(messages) {
  if (messages.length === 0) {
    nodes.steps.replaceChildren(h("li", { class: "pending" }, "Aguardando os serviços..."));
    return;
  }
  nodes.steps.replaceChildren(...messages.map((text) => h("li", {}, text)));
}

function render(order) {
  nodes.stepper.replaceChildren(stepper(order));
  renderSteps(order.notifications ?? []);
}

function finish(order) {
  const confirmed = order.status === "CONFIRMED";
  nodes.pulse.className = `pulse ${order.status.toLowerCase()}`;
  nodes.title.textContent = headline(order);
  nodes.detail.textContent = confirmed
    ? `Pagamento processado pela instância ${order.processed_by}.`
    : `${reasonLabel(order.reason)}. Processado pela instância ${order.processed_by}.`;
  nodes.done.hidden = false;
  refresh();
}

function giveUp() {
  nodes.pulse.className = "pulse";
  nodes.title.textContent = "O pedido ainda está em processamento";
  nodes.detail.textContent = "Você pode fechar esta janela e acompanhar em Meus ingressos.";
  nodes.done.hidden = false;
}

async function poll(id, attempt) {
  try {
    const order = await getOrder(id);
    render(order);
    if (order.status !== "PROCESSING") {
      finish(order);
      return;
    }
  } catch (error) {
    nodes.detail.textContent = error.message;
  }
  if (attempt >= config.pollMax) {
    giveUp();
    return;
  }
  timer = setTimeout(() => poll(id, attempt + 1), config.pollMs);
}

function track(accepted) {
  nodes.info.querySelector(".checkout-details").hidden = true;
  nodes.form.hidden = true;
  nodes.tracker.hidden = false;
  nodes.done.hidden = true;
  nodes.pulse.className = "pulse active";
  nodes.title.textContent = accepted.message;
  nodes.detail.textContent = `Pedido ${accepted.order_id.slice(0, 8)}`;
  render({ status: "PROCESSING", stage: "RECEIVED", notifications: [] });
  refresh();
  poll(accepted.order_id, 0);
}

async function submit(event) {
  event.preventDefault();
  if (!isLogged()) {
    goLogin();
    return;
  }
  nodes.error.hidden = true;
  nodes.submit.disabled = true;
  try {
    track(await createOrder(readForm()));
  } catch (error) {
    nodes.error.textContent = error.message;
    nodes.error.hidden = false;
  } finally {
    nodes.submit.disabled = false;
  }
}

export function openCheckout(selectedTicket, onChange) {
  ticket = selectedTicket;
  refresh = onChange;
  stop();
  nodes.form.reset();
  nodes.form.hidden = false;
  nodes.tracker.hidden = true;
  nodes.error.hidden = true;
  nodes.banner.replaceChildren(cover(ticket.image, "banner"));
  nodes.info.replaceChildren(...detail(ticket));
  nodes.types.replaceChildren(
    h("legend", {}, "Tipo de ingresso"),
    ...ticket.types.map(option),
  );
  const buyable = !ticket.sold_out && ticket.open;
  nodes.notice.textContent = ticket.sold_out ? "Ingressos esgotados." : "As vendas deste evento foram encerradas.";
  nodes.notice.hidden = buyable;
  nodes.form.querySelectorAll("input, button[type=submit]").forEach((node) => {
    node.disabled = !buyable;
  });
  nodes.submit.textContent = isLogged() ? "Comprar ingressos" : "Entrar para comprar";
  nodes.scroll.scrollTop = 0;
  updateTotal();
  nodes.dialog.showModal();
}

nodes.form.addEventListener("submit", submit);
nodes.form.elements.quantity.addEventListener("input", updateTotal);
nodes.close.addEventListener("click", () => nodes.dialog.close());
nodes.done.addEventListener("click", () => nodes.dialog.close());
nodes.dialog.addEventListener("close", stop);
nodes.dialog.addEventListener("click", (event) => {
  if (event.target === nodes.dialog) {
    nodes.dialog.close();
  }
});
