const node = document.querySelector("#toast");
let timer = null;

export function toast(text) {
  node.textContent = text;
  node.hidden = false;
  clearTimeout(timer);
  timer = setTimeout(() => {
    node.hidden = true;
  }, 4000);
}