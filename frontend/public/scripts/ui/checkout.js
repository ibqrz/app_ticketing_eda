import { createOrder, getOrder } from "../api/orders.js";
import { config } from "../config.js";
import { h } from "./dom.js";
import { money, reasonLabel } from "./format.js";

const find = (selector) => document.querySelector(selector);

const nodes = {
  dialog: find("#checkout"),
  form: find("#checkout-form"),
  summary: find("#checkout-summary"),
  total: find("#checkout-total"),
  error: find("#checkout-error"),
  submit: find("#checkout-submit"),
  close: find("#checkout-close"),
  tracker: find("#tracker"),
  pulse: find("#tracker-pulse"),
  title: find("#tracker-title"),
  detail: find("#tracker-detail"),
  steps: find("#tracker-steps"),
  done: find("#tracker-done"),
};

let ticket = null;
let timer = null;
let refresh = () => {};

function stop() {
  clearTimeout(timer);
}

function updateTotal() {
  const quantity = Number(nodes.form.elements.quantity.value) || 0;
  nodes.total.textContent = money(ticket.price * quantity);
}

function readForm() {
  const data = new FormData(nodes.form);
  return {
    ticket_type_id: ticket.id,
    quantity: Number(data.get("quantity")),
    customer_name: String(data.get("customer_name")).trim(),
    customer_email: String(data.get("customer_email")).trim(),
  };
}

function renderSteps(messages) {
  if (messages.length === 0) {
    nodes.steps.replaceChildren(h("li", { class: "pending" }, "Aguardando os serviços..."));
    return;
  }
  nodes.steps.replaceChildren(...messages.map((text) => h("li", {}, text)));
}

function finish(order) {
  const confirmed = order.status === "CONFIRMED";
  nodes.pulse.className = `pulse ${order.status.toLowerCase()}`;
  nodes.title.textContent = confirmed ? "Pedido confirmado" : "Pedido recusado";
  nodes.detail.textContent = confirmed
    ? `Pagamento processado pela instância ${order.processed_by}.`
    : `${reasonLabel(order.reason)}. Processado pela instância ${order.processed_by}.`;
  nodes.done.hidden = false;
  refresh();
}

function giveUp() {
  nodes.pulse.className = "pulse";
  nodes.title.textContent = "O pedido ainda está em processamento";
  nodes.detail.textContent = "Você pode fechar esta janela e acompanhar em Pedidos recentes.";
  nodes.done.hidden = false;
}

async function poll(id, attempt) {
  try {
    const order = await getOrder(id);
    renderSteps(order.notifications);
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
  nodes.form.hidden = true;
  nodes.tracker.hidden = false;
  nodes.done.hidden = true;
  nodes.pulse.className = "pulse active";
  nodes.title.textContent = accepted.message;
  nodes.detail.textContent = `Pedido ${accepted.order_id.slice(0, 8)}`;
  renderSteps([]);
  refresh();
  poll(accepted.order_id, 0);
}

async function submit(event) {
  event.preventDefault();
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

export function openCheckout(event, selected, onChange) {
  ticket = selected;
  refresh = onChange;
  stop();
  nodes.form.reset();
  nodes.form.hidden = false;
  nodes.tracker.hidden = true;
  nodes.error.hidden = true;
  nodes.summary.textContent = `${event.title}, ${selected.name}`;
  updateTotal();
  nodes.dialog.showModal();
}

nodes.form.addEventListener("submit", submit);
nodes.form.elements.quantity.addEventListener("input", updateTotal);
nodes.close.addEventListener("click", () => nodes.dialog.close());
nodes.done.addEventListener("click", () => nodes.dialog.close());
nodes.dialog.addEventListener("close", stop);
