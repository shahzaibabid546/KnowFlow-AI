export type ChatMessage = {
  message_id?: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  created_at?: string;
};

export type ChatSession = {
  session_id: string;
  messages?: ChatMessage[];
  created_at?: string;
  updated_at?: string;
};

export type ChatReply = {
  session_id: string;
  answer: string;
  sources: string[];
  answer_status?: string;
  retry_count?: number;
  needs_human?: boolean;
  escalation_reason?: string;
};

export type Ticket = {
  ticket_id: string;
  customer_id: string;
  session_id: string;
  subject: string;
  description: string;
  status: "open" | "in_progress" | "resolved" | "closed";
  priority: "low" | "normal" | "high" | "urgent";
  assigned_to?: string | null;
  created_at?: string;
  updated_at?: string;
};

export type TicketCreate = {
  customer_id: string;
  session_id: string;
  subject: string;
  description: string;
  priority: "low" | "normal" | "high" | "urgent";
};
