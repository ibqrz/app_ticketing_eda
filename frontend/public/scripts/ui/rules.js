import { h } from "./dom.js";
import { icon } from "./icons.js";

const RULES = [
  { text: "Mínimo de 8 caracteres", ok: (value) => value.length >= 8 },
  { text: "Uma letra maiúscula", ok: (value) => /[A-Z]/.test(value) },
  { text: "Um número", ok: (value) => /\d/.test(value) },
  { text: "Um caractere especial", ok: (value) => /[^A-Za-z0-9]/.test(value) },
];

export function mountRules(input, list) {
  const items = RULES.map((rule) => ({
    rule,
    node: h("li", {}, h("span", { class: "mark" }, icon("check", 12)), h("span", {}, rule.text)),
  }));
  list.replaceChildren(...items.map((item) => item.node));

  const update = () => {
    for (const item of items) {
      item.node.classList.toggle("met", item.rule.ok(input.value));
    }
  };

  input.addEventListener("input", update);
  input.form?.addEventListener("reset", () => setTimeout(update));
  update();
  return () => items.every((item) => item.rule.ok(input.value));
}