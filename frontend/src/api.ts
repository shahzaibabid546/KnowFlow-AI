
import axios from "axios";
import type { ChatReply, ChatSession, Ticket, TicketCreate } from "./types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  timeout: 60000,
});

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;

    if (typeof detail === "string") return detail;
    if (detail) return JSON.stringify(detail);

    if (error.code === "ECONNREFUSED" || error.code === "ERR_NETWORK") {
      return "Backend se connection nahi ho raha. Check karein ke FastAPI server chal raha hai.";
    }

    return error.message;
  }

  return error instanceof Error
    ? error.message
    : "Unexpected error occurred.";
}

export const apiService = {
  health: async () => (await api.get("/health")).data,

  createSession: async (): Promise<ChatSession> =>
    (await api.post("/chat/sessions")).data,

  sendMessage: async (
    sessionId: string,
    content: string
  ): Promise<ChatReply> =>
    (
      await api.post(
        `/chat/sessions/${encodeURIComponent(sessionId)}/messages`,
        null,
        { params: { content } }
      )
    ).data,

  getSession: async (sessionId: string): Promise<ChatSession> =>
    (await api.get(`/chat/sessions/${encodeURIComponent(sessionId)}`)).data,

  deleteSession: async (sessionId: string) =>
    (await api.delete(`/chat/sessions/${encodeURIComponent(sessionId)}`)).data,

  listTickets: async (): Promise<Ticket[]> => {
    const response = await api.get("/tickets/");
    return response.data.tickets;
  },

  createTicket: async (ticket: TicketCreate): Promise<Ticket> =>
    (await api.post("/tickets/", ticket)).data,

  updateTicket: async (ticketId: string, updates: Partial<Ticket>) =>
    (await api.patch(`/tickets/${encodeURIComponent(ticketId)}`, updates)).data,

  deleteTicket: async (ticketId: string) =>
    (await api.delete(`/tickets/${encodeURIComponent(ticketId)}`)).data,

  uploadDocument: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return (await api.post("/documents/upload", form)).data;
  },
};

export default api;
