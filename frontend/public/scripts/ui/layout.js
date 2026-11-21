import { logout } from "../api/auth.js";
import { config } from "../config.js";
import { clear, isLogged, user } from "../state/session.js";
import { avatar } from "./avatar.js";
import { find, h } from "./dom.js";
import { icon } from "./icons.js";

const HOME = { key: "home", href: "index.html", label: "Eventos", icon: "calendar" };

const LOGGED = [
  HOME,
  { key: "orders", href: "orders.html", label: "Meus ingressos", icon: "ticket" },
];

const GUEST = [HOME, { key: "login", href: "login.html", label: "Entrar", icon: "login" }];

function link(item, active) {
  return h(
    "a",
    {
      href: item.href,
      title: item.label,
      "aria-current": item.key === active ? "page" : false,
    },
    icon(item.icon, 20),
    h("span", { class: "label" }, item.label),
  );
}

function leave() {
  logout()
    .catch(() => null)
    .finally(() => {
      clear();
      location.href = "index.html";
    });
}

function exit() {
  return h(
    "button",
    { type: "button", title: "Sair", "aria-label": "Sair", onclick: leave },
    icon("logout", 20),
    h("span", { class: "label" }, "Sair"),
  );
}

export function renderLayout(active, title) {
  document.title = title ? `${config.brandName} | ${title}` : config.brandName;
  const logged = isLogged();
  const items = (logged ? LOGGED : GUEST).map((item) => link(item, active));
  find("#app-header").replaceChildren(
    h(
      "div",
      { class: "wrap topbar-inner" },
      h(
        "a",
        { class: "brand", href: "index.html" },
        h("img", {
          class: "brand-logo",
          src: config.brandLogo,
          alt: config.brandLogoAlt,
          height: "46",
        }),
        h("span", { class: "brand-name" }, config.brandName),
      ),
      h(
        "nav",
        { class: "nav", "aria-label": "Principal" },
        items,
        logged ? avatar(user(), active === "account") : null,
        logged ? exit() : null,
      ),
    ),
  );
  find("#app-footer").replaceChildren(
    h(
      "div",
      { class: "wrap" },
      h("p", {}, `© ${new Date().getFullYear()} ${config.brandName}. Todos os direitos reservados.`),
    ),
  );
}
