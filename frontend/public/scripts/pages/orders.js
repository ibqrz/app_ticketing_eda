import { listOrders } from "../api/orders.js";
import { config } from "../config.js";
import { goLogin, isLogged } from "../state/session.js";
import { empty, find } from "../ui/dom.js";
import { renderLayout } from "../ui/layout.js";
import { isLive } from "../ui/format.js";
import { orderCard } from "../ui/orderCard.js";
import { openOrder } from "../ui/orderDialog.js";
import { progressCard } from "../ui/progress.js";
import { toast } from "../ui/toast.js";

renderLayout("orders", "Meus ingressos");

const tabs = {
  orders: { tab: find("#tab-orders"), panel: find("#panel-orders") },
  tracking: { tab: find("#tab-tracking"), panel: find("#panel-tracking") },
};

const snapshot = {};

const open = (order) => openOrder(order, () => load(true));

function select(name) {
  for (const [key, item] of Object.entries(tabs)) {
    const on = key === name;
    item.tab.setAttribute("aria-selected", String(on));
    item.tab.tabIndex = on ? 0 : -1;
    item.panel.hidden = !on;
  }
  history.replaceState(null, "", name === "tracking" ? "#tracking" : location.pathname);
}

function badge(node, total) {
  node.textContent = String(total);
  node.hidden = total === 0;
}

function changed(key, data) {
  const text = JSON.stringify(data);
  if (snapshot[key] === text) {
    return false;
  }
  snapshot[key] = text;
  return true;
}

function fill(grid, orders, text) {
  if (orders.length === 0) {
    grid.replaceChildren(empty(text));
    return;
  }
  grid.replaceChildren(...orders.map((order) => orderCard(order, open)));
}

function renderPurchased(orders) {
  badge(find("#count-orders"), orders.length);
  const none = orders.length === 0;
  find("#orders-empty").hidden = !none;
  find("#orders-empty").replaceChildren(...(none ? [empty("Nenhum ingresso comprado")] : []));
  find("#active-block").hidden = none;
  find("#inactive-block").hidden = none;
  fill(find("#grid-active"), orders.filter(isLive), "Nenhum ingresso ativo");
  fill(find("#grid-inactive"), orders.filter((order) => !isLive(order)), "Nenhum ingresso inativo");
}

function renderTracking(orders) {
  badge(find("#count-tracking"), orders.filter((order) => order.status === "PROCESSING").length);
  const grid = find("#grid-tracking");
  if (orders.length === 0) {
    grid.replaceChildren(empty("Nenhum pedido em processamento"));
    return;
  }
  grid.replaceChildren(...orders.map(progressCard));
}

async function load(quiet = false) {
  try {
    const [purchased, tracking] = await Promise.all([
      listOrders("purchased", 100),
      listOrders("tracking", 30),
    ]);
    if (changed("purchased", purchased)) {
      renderPurchased(purchased);
    }
    if (changed("tracking", tracking)) {
      renderTracking(tracking);
    }
  } catch (error) {
    if (!quiet) {
      toast(error.message);
    }
  }
}

function keys(event) {
  const order = ["orders", "tracking"];
  const index = order.findIndex((name) => tabs[name].tab === document.activeElement);
  if (index < 0 || !["ArrowLeft", "ArrowRight"].includes(event.key)) {
    return;
  }
  const next = order[(index + (event.key === "ArrowRight" ? 1 : order.length - 1)) % order.length];
  select(next);
  tabs[next].tab.focus();
}

if (!isLogged()) {
  goLogin();
} else {
  tabs.orders.tab.addEventListener("click", () => select("orders"));
  tabs.tracking.tab.addEventListener("click", () => select("tracking"));
  find(".tabs").addEventListener("keydown", keys);
  select(location.hash === "#tracking" ? "tracking" : "orders");
  load();
  setInterval(() => {
    if (!document.hidden) {
      load(true);
    }
  }, config.trackMs);
}