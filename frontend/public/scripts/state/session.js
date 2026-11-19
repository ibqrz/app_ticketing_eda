const KEY = "voucher.session";

export function read() {
  try {
    return JSON.parse(localStorage.getItem(KEY));
  } catch {
    return null;
  }
}

export const token = () => read()?.token ?? null;

export const user = () => read()?.user ?? null;

export const isLogged = () => token() !== null;

export function save(session) {
  localStorage.setItem(KEY, JSON.stringify(session));
}

export function updateUser(data) {
  const session = read();
  if (session) {
    save({ ...session, user: data });
  }
}

export function clear() {
  localStorage.removeItem(KEY);
}

export function goLogin() {
  const page = location.pathname.split("/").pop() || "index.html";
  location.href = `login.html?next=${encodeURIComponent(page + location.hash)}`;
}
