import { request } from "./http.js";

export const createOrder = (data) =>
  request("/api/orders", { method: "POST", body: JSON.stringify(data) });

export const refundTicket = (id) => request(`/api/orders/${id}/refunds`, { method: "POST" });

export const getOrder = (id) => request(`/api/orders/${id}`);

export const listOrders = (scope = "purchased", limit = 10) =>
  request(`/api/orders?scope=${scope}&limit=${limit}`);
