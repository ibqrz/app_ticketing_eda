import { request } from "./http.js";

export const listEvents = () => request("/api/events");