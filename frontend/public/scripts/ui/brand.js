import { config } from "../config.js";

export function applyBrand() {
  document.title = config.brandName;
  document.querySelectorAll("[data-brand-name]").forEach((node) => {
    node.textContent = config.brandName;
  });
  document.querySelectorAll("[data-brand-logo]").forEach((node) => {
    node.src = config.brandLogo;
    node.alt = config.brandLogoAlt;
  });
}