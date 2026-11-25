import { useEffect, useState } from "react";
import { ArrowUpRight, BookOpen, CheckCircle2, FileText, MessageSquare, Plus, Sparkles, Ticket, UploadCloud } from "lucide-react";
import { Link } from "react-router-dom";
import { apiService, getErrorMessage } from "../api";
import type { Ticket as TicketType } from "../types";

export default function Overview({ backendStatus }: { backendStatus: string }) {
  const [tickets, setTickets] = useState<TicketType[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiService.listTickets()
      .then(setTickets)
      .catch((e) => setError(getErrorMessage(e)))
      .finally(() => setLoading(false));
  }, []);

  const openTickets = tickets.filter(t => t.status === "open" || t.status === "in_progress").length;
  const stats = [
    { label: "Support tickets", value: loading ? "—" : String(tickets.length), note: "Total in workspace", icon: Ticket, tone: "violet" },
    { label: "Open tickets", value: loading ? "—" : String(openTickets), note: "Needs attention", icon: MessageSquare, tone: "blue" },
    { label: "Knowledge sources", value: "—", note: "Upload documents to begin", icon: BookOpen, tone: "green" },
    { label: "AI service", value: backendStatus === "online" ? "Online" : backendStatus === "offline" ? "Offline" : "Checking", note: "FastAPI health status", icon: Sparkles, tone: "amber" },
  ];

  return <div className="page-stack">
    <section className="welcome-row">
      <div><div className="eyebrow"><Sparkles size={14}/> YOUR AI KNOWLEDGE WORKSPACE</div><h1>Good to see you again.</h1><p>Here’s what’s happening across your customer support workspace.</p></div>
      <Link to="/chat" className="button button-primary"><Plus size={17}/> Start a conversation</Link>
    </section>

    <section className="stats-grid">
      {stats.map(({label,value,note,icon:Icon,tone}) => <div className="stat-card" key={label}>
        <div className={`stat-icon ${tone}`}><Icon size={19}/></div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-note">{note}</div>
      </div>)}
    </section>

    <section className="overview-grid">
      <div className="panel welcome-panel">
        <div className="panel-heading"><div><div className="eyebrow">GETTING STARTED</div><h2>Build your knowledge workspace</h2><p>Bring your company information together and let AI help your customers.</p></div><div className="panel-heading-icon"><Sparkles size={20}/></div></div>
        <div className="setup-list">
          <Link to="/documents" className="setup-item"><div className="setup-number"><UploadCloud size={18}/></div><div><strong>Upload your knowledge documents</strong><small>Add PDF and TXT files with your policies and FAQs.</small></div><ArrowUpRight size={17}/></Link>
          <Link to="/chat" className="setup-item"><div className="setup-number"><MessageSquare size={18}/></div><div><strong>Try your AI support assistant</strong><small>Ask a question and see answers grounded in your documents.</small></div><ArrowUpRight size={17}/></Link>
          <Link to="/tickets" className="setup-item"><div className="setup-number"><Ticket size={18}/></div><div><strong>Manage customer support tickets</strong><small>Track, prioritize and update customer requests.</small></div><ArrowUpRight size={17}/></Link>
        </div>
      </div>

      <div className="panel quick-panel">
        <div className="panel-title-row"><div><h2>Quick actions</h2><p>Jump back into your workflow.</p></div></div>
        <Link to="/documents" className="quick-action"><span className="quick-icon green"><FileText size={18}/></span><span><strong>Upload a document</strong><small>PDF or TXT</small></span><ArrowUpRight size={16}/></Link>
        <Link to="/chat" className="quick-action"><span className="quick-icon blue"><MessageSquare size={18}/></span><span><strong>Ask the AI assistant</strong><small>Get a grounded answer</small></span><ArrowUpRight size={16}/></Link>
        <Link to="/tickets" className="quick-action"><span className="quick-icon violet"><Ticket size={18}/></span><span><strong>Create a support ticket</strong><small>Track customer issues</small></span><ArrowUpRight size={16}/></Link>
        <div className="tip-box"><Sparkles size={16}/><p><strong>Pro tip</strong><br/>Keep your policies and FAQs up to date for more helpful AI responses.</p></div>
      </div>
    </section>

    <section className="panel ticket-preview">
      <div className="panel-title-row"><div><h2>Recent support tickets</h2><p>Latest activity from your support queue.</p></div><Link to="/tickets" className="text-link">View all <ArrowUpRight size={14}/></Link></div>
      {error ? <div className="inline-error">{error}</div> : loading ? <div className="empty-state compact">Loading tickets…</div> : tickets.length === 0 ? <div className="empty-state compact"><Ticket size={24}/><strong>No tickets yet</strong><span>New support tickets will appear here.</span></div> : <div className="table-wrap"><table><thead><tr><th>SUBJECT</th><th>CUSTOMER</th><th>PRIORITY</th><th>STATUS</th></tr></thead><tbody>{tickets.slice(0,5).map(t=><tr key={t.ticket_id}><td className="table-primary">{t.subject}</td><td>{t.customer_id}</td><td><span className={`priority ${t.priority}`}>{t.priority}</span></td><td><span className={`status-badge ${t.status}`}>{t.status.replace("_"," ")}</span></td></tr>)}</tbody></table></div>}
    </section>
  </div>;
}
