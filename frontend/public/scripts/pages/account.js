import { changePassword, getAccount, updateAccount } from "../api/account.js";
import { goLogin, isLogged, updateUser } from "../state/session.js";
import { find } from "../ui/dom.js";
import { mountFields } from "../ui/field.js";
import { renderLayout } from "../ui/layout.js";
import { mountRules } from "../ui/rules.js";
import { toast } from "../ui/toast.js";

renderLayout("account", "Minha conta");
mountFields();

const profile = find("#profile-form");
const password = find("#password-form");
const valid = mountRules(password.elements.new_password, find("#password-rules"));

function show(node, text) {
  node.textContent = text;
  node.hidden = false;
}

function stats(user) {
  const total = user.tickets.length;
  find("#account-stats").textContent =
    total === 0 ? "Você ainda não possui ingressos." : `Você possui ${total} ingresso(s) confirmado(s).`;
}

async function load() {
  try {
    const user = await getAccount();
    profile.elements.name.value = user.name;
    profile.elements.email.value = user.email;
    updateUser(user);
    stats(user);
  } catch (error) {
    toast(error.message);
  }
}

async function saveProfile(event) {
  event.preventDefault();
  find("#profile-error").hidden = true;
  find("#profile-success").hidden = true;
  try {
    const user = await updateAccount({
      name: profile.elements.name.value.trim(),
      email: profile.elements.email.value.trim(),
    });
    updateUser(user);
    show(find("#profile-success"), "Dados atualizados com sucesso.");
  } catch (error) {
    show(find("#profile-error"), error.message);
  }
}

async function savePassword(event) {
  event.preventDefault();
  find("#password-error").hidden = true;
  find("#password-success").hidden = true;
  const form = password.elements;
  if (!valid()) {
    show(find("#password-error"), "A nova senha não atende a todos os requisitos.");
    return;
  }
  if (form.new_password.value !== form.confirm_password.value) {
    show(find("#password-error"), "A confirmação da nova senha não confere.");
    return;
  }
  try {
    await changePassword({
      current_password: form.current_password.value,
      new_password: form.new_password.value,
    });
    password.reset();
    show(find("#password-success"), "Senha atualizada com sucesso.");
  } catch (error) {
    show(find("#password-error"), error.message);
  }
}

if (!isLogged()) {
  goLogin();
} else {
  profile.addEventListener("submit", saveProfile);
  password.addEventListener("submit", savePassword);
  load();
}