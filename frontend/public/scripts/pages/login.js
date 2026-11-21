import { login, register } from "../api/auth.js";
import { isLogged, save } from "../state/session.js";
import { find } from "../ui/dom.js";
import { mountFields } from "../ui/field.js";
import { renderLayout } from "../ui/layout.js";
import { mountRules } from "../ui/rules.js";

renderLayout("login", "Entrar");
mountFields();

const modes = {
  login: { tab: find("#mode-login"), form: find("#login-form"), error: find("#login-error") },
  register: { tab: find("#mode-register"), form: find("#register-form"), error: find("#register-error") },
};

function destination() {
  const next = new URLSearchParams(location.search).get("next") ?? "";
  return /^[a-z]+\.html(#[a-z]+)?$/.test(next) ? next : "index.html";
}

function select(name) {
  for (const [key, mode] of Object.entries(modes)) {
    mode.tab.setAttribute("aria-selected", String(key === name));
    mode.form.hidden = key !== name;
    mode.error.hidden = true;
  }
}

function submit(name, action, read, check = () => null) {
  const mode = modes[name];
  mode.form.addEventListener("submit", async (event) => {
    event.preventDefault();
    mode.error.hidden = true;
    try {
      const problem = check();
      if (problem) {
        throw new Error(problem);
      }
      save(await action(read(mode.form.elements)));
      location.href = destination();
    } catch (error) {
      mode.error.textContent = error.message;
      mode.error.hidden = false;
    }
  });
}

if (isLogged()) {
  location.href = destination();
}

modes.login.tab.addEventListener("click", () => select("login"));
modes.register.tab.addEventListener("click", () => select("register"));

submit("login", login, (form) => ({
  email: form.email.value.trim(),
  password: form.password.value,
}));

const valid = mountRules(modes.register.form.elements.password, find("#register-rules"));

submit(
  "register",
  register,
  (form) => ({
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    password: form.password.value,
  }),
  () => (valid() ? null : "A senha não atende a todos os requisitos."),
);
