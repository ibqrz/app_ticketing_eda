import { request } from "./http.js";

const post = (path, data) => request(path, { method: "POST", body: JSON.stringify(data) });

export const register = (data) => post("/api/auth/register", data);

export const login = (data) => post("/api/auth/login", data);

export const logout = () => request("/api/auth/logout", { method: "POST" });