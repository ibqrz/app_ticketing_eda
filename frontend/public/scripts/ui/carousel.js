import { h } from "./dom.js";
import { icon } from "./icons.js";

const wrap = (items) => items.map((item) => h("div", { class: "carousel-item" }, item));

function build(items) {
  const track = h("div", { class: "carousel-track", tabindex: "0" }, wrap(items));
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

  prev.disabled = true;
  next.disabled = true;
  prev.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  track.addEventListener("scroll", update, { passive: true });
  new ResizeObserver(update).observe(track);
  return { root, track, update };
}

export function mountCarousel(container, items) {
  const track = container.querySelector(".carousel-track");
  if (track) {
    const left = track.scrollLeft;
    track.replaceChildren(...wrap(items));
    track.scrollLeft = left;
    track.dispatchEvent(new Event("scroll"));
    return;
  }
  const built = build(items);
  container.replaceChildren(built.root);
  built.update();
}