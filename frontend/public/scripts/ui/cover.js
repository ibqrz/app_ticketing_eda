import { config } from "../config.js";
import { h } from "./dom.js";
import { icon } from "./icons.js";

const source = (image) => (image.startsWith("/") ? config.apiUrl + image : image);

export function cover(image, extra = "") {
  const node = h("div", { class: `cover ${extra}`.trim() }, icon("ticket", 48));
  if (image) {
    const picture = h("img", { src: source(image), alt: "", loading: "lazy" });
    picture.addEventListener("error", () => picture.remove());
    node.append(picture);
  }
  return node;
}