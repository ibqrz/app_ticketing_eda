import { h } from "./dom.js";

const TONES = ["#1c63d9", "#0f6b47", "#a8223b", "#6b3fa0", "#b24a00", "#00707a", "#8c3a7a", "#4a5a8a"];

export function initials(name) {
  const parts = String(name ?? "").trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) {
    return "?";
  }
  const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
  return (parts[0][0] + last).toUpperCase();
}

export function tone(id) {
  return TONES[Math.abs(Number(id) || 0) % TONES.length];
}

export function avatar(person, current) {
  return h(
    "a",
    {
      class: "avatar",
      href: "account.html",
      title: "Minha conta",
      "aria-label": "Minha conta",
      "aria-current": current ? "page" : false,
      style: `background:${tone(person?.id)}`,
    },
    initials(person?.name),
  );
}
