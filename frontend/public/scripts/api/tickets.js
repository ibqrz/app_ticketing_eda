import { request } from "./http.js";

export const listTickets = () => request("/api/tickets");
