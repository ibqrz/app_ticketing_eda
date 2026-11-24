import { request } from "./http.js";

export const getAccount = () => request("/api/account");

export const updateAccount = (data) =>
  request("/api/account", { method: "PATCH", body: JSON.stringify(data) });

export const changePassword = (data) =>
  request("/api/account/password", { method: "PUT", body: JSON.stringify(data) });