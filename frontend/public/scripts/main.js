import { listEvents } from "./api/events.js";
import { listOrders } from "./api/orders.js";
import { config } from "./config.js";
import { applyBrand } from "./ui/brand.js";
import { renderCatalog } from "./ui/catalog.js";
import { openCheckout } from "./ui/checkout.js";
import { renderOrders } from "./ui/history.js";
import { toast } from "./ui/toast.js";

const catalog = document.querySelector("#catalog");
const body = document.querySelector("#orders-body");
const empty = document.querySelector("#orders-empty");

async function loadCatalog() {
  try {
    renderCatalog(catalog, await listEvents(), buy);
  } catch (error) {
    toast(error.message);
  }
}

async function loadOrders(quiet = false) {
  try {
    renderOrders(body, empty, await listOrders(10));
  } catch (error) {
    if (!quiet) {
      toast(error.message);
    }
  }
}

function refresh() {
  loadCatalog();
  loadOrders();
}

function buy(event, ticket) {
  openCheckout(event, ticket, refresh);
}

applyBrand();
refresh();
setInterval(() => loadOrders(true), config.refreshMs);
