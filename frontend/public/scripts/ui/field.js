import { h } from "./dom.js";
import { icon } from "./icons.js";

function eye(input) {
  const button = h(
    "button",
    { type: "button", class: "eye", "aria-label": "Mostrar senha", "aria-pressed": "false" },
    icon("eye", 20),
  );
  button.addEventListener("click", () => {
    const shown = input.type === "password";
    input.type = shown ? "text" : "password";
    button.setAttribute("aria-label", shown ? "Ocultar senha" : "Mostrar senha");
    button.setAttribute("aria-pressed", String(shown));
    button.replaceChildren(icon(shown ? "eyeOff" : "eye", 20));
  });
  return button;
}

export function mountFields() {
  document.querySelectorAll(".field.float input[type=password]").forEach((input) => {
    const field = input.closest(".field");
    field.classList.add("has-eye");
    field.append(eye(input));
  });
}
