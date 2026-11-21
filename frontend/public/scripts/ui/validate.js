const REQUIRED = "Preencha os campos obrigatórios";

function problem(input) {
  if (input.required && input.value.trim() === "") {
    return REQUIRED;
  }
  if (input.validity.typeMismatch) {
    return "Informe um e-mail válido.";
  }
  if (!input.checkValidity()) {
    return input.validationMessage;
  }
  return null;
}

export function mountValidation(form) {
  form.noValidate = true;
  form.addEventListener("input", (event) => {
    const field = event.target.closest(".field");
    field?.classList.remove("invalid");
    event.target.removeAttribute("aria-invalid");
  });
}

export function validate(form) {
  const found = [];
  let first = null;
  for (const input of form.querySelectorAll("input")) {
    const text = problem(input);
    input.closest(".field")?.classList.toggle("invalid", text !== null);
    input.toggleAttribute("aria-invalid", text !== null);
    if (text) {
      found.push(text);
      first ??= input;
    }
  }
  first?.focus();
  return found.includes(REQUIRED) ? REQUIRED : (found[0] ?? null);
}