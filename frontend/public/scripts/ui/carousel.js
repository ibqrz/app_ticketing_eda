import { h } from "./dom.js";
import { icon } from "./icons.js";

function build(items) {
  const track = h(
    "div",
    { class: "carousel-track", tabindex: "0" },
    items.map((item) => h("div", { class: "carousel-item" }, item)),
  );
  const prev = h(
    "button",
    { type: "button", class: "carousel-btn prev", "aria-label": "Eventos anteriores" },
    icon("left", 22),
  );
  const next = h(
    "button",
    { type: "button", class: "carousel-btn next", "aria-label": "Próximos eventos" },
    icon("right", 22),
  );
  const root = h(
    "div",
    {
      class: "carousel",
      role: "region",
      "aria-roledescription": "carrossel",
      "aria-label": "Eventos disponíveis",
    },
    prev,
    track,
    next,
  );

  const update = () => {
    prev.disabled = track.scrollLeft <= 4;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    root.classList.toggle("fits", track.scrollWidth <= track.clientWidth + 4);
  };
  const move = (direction) =>
    track.scrollBy({ left: direction * track.clientWidth * 0.9, behavior: "smooth" });

  prev.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  track.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  return { root, track, update };
}

export function mountCarousel(container, items) {
  const previous = container.querySelector(".carousel-track")?.scrollLeft ?? 0;
  const { root, track, update } = build(items);
  container.replaceChildren(root);
  track.scrollLeft = previous;
  update();
}
