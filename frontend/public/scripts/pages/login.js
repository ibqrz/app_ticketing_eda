import { login, register } from "../api/auth.js";
import { isLogged, save } from "../state/session.js";
import { find } from "../ui/dom.js";
import { renderLayout } from "../ui/layout.js";

renderLayout("login", "Entrar");

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

function submit(name, action, read) {
  const mode = modes[name];
  mode.form.addEventListener("submit", async (event) => {
    event.preventDefault();
    mode.error.hidden = true;
    try {
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

submit("register", register, (form) => ({
  name: form.name.value.trim(),
  email: form.email.value.trim(),
  password: form.password.value,
}));
