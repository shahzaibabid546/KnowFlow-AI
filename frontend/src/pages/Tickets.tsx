import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { AlertCircle, Plus, RefreshCw, Search, Ticket as TicketIcon, X } from "lucide-react";
import { apiService, getErrorMessage } from "../api";
import type { Ticket } from "../types";

const blank = { customer_id:"", session_id:"", subject:"", description:"", priority:"normal" as Ticket["priority"] };

export default function Tickets() {
  const [tickets,setTickets] = useState<Ticket[]>([]);
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState("");
  const [query,setQuery] = useState("");
  const [statusFilter,setStatusFilter] = useState("all");
  const [showForm,setShowForm] = useState(false);
  const [form,setForm] = useState(blank);
  const [saving,setSaving] = useState(false);

  async function load() {
    setLoading(true); setError("");
    try { setTickets(await apiService.listTickets()); }
    catch(e) { setError(getErrorMessage(e)); }
    finally { setLoading(false); }
  }
  useEffect(()=>{void load();},[]);

  async function create(e:FormEvent) {
    e.preventDefault(); setSaving(true); setError("");
    try { await apiService.createTicket(form); setForm(blank); setShowForm(false); await load(); }
    catch(e) { setError(getErrorMessage(e)); }
    finally { setSaving(false); }
  }
  async function updateStatus(ticket:Ticket,status:Ticket["status"]) {
    try { await apiService.updateTicket(ticket.ticket_id,{status}); await load(); }
    catch(e) { setError(getErrorMessage(e)); }
  }
  async function remove(ticket:Ticket) {
    if(!window.confirm(`Delete ticket "${ticket.subject}"?`)) return;
    try { await apiService.deleteTicket(ticket.ticket_id); await load(); }
    catch(e) { setError(getErrorMessage(e)); }
  }

  const filtered = tickets.filter(t => (statusFilter==="all"||t.status===statusFilter) && `${t.subject} ${t.customer_id} ${t.ticket_id}`.toLowerCase().includes(query.toLowerCase()));

  return <div className="page-stack">
    <section className="page-heading-row"><div><div className="eyebrow"><TicketIcon size={14}/> CUSTOMER SUPPORT</div><h1>Support Tickets</h1><p>Create, prioritize and track customer support requests.</p></div><button className="button button-primary" onClick={()=>setShowForm(true)}><Plus size={17}/> New ticket</button></section>
    <section className="ticket-metrics">
      <div className="mini-stat"><span>Total tickets</span><strong>{tickets.length}</strong></div>
      <div className="mini-stat"><span>Open</span><strong>{tickets.filter(t=>t.status==="open").length}</strong></div>
      <div className="mini-stat"><span>In progress</span><strong>{tickets.filter(t=>t.status==="in_progress").length}</strong></div>
      <div className="mini-stat"><span>Resolved</span><strong>{tickets.filter(t=>t.status==="resolved"||t.status==="closed").length}</strong></div>
    </section>
    <section className="panel">
      <div className="ticket-controls"><div className="search-field"><Search size={16}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search tickets…"/></div><select value={statusFilter} onChange={e=>setStatusFilter(e.target.value)}><option value="all">All statuses</option><option value="open">Open</option><option value="in_progress">In progress</option><option value="resolved">Resolved</option><option value="closed">Closed</option></select><button className="button button-secondary button-small" onClick={load}><RefreshCw size={14}/> Refresh</button></div>
      {error && <div className="inline-error"><AlertCircle size={16}/>{error}</div>}
      {loading ? <div className="empty-state">Loading tickets…</div> : filtered.length===0 ? <div className="empty-state"><TicketIcon size={27}/><strong>No matching tickets</strong><span>Create a ticket or change your search filters.</span></div> : <div className="table-wrap"><table><thead><tr><th>SUBJECT</th><th>CUSTOMER</th><th>PRIORITY</th><th>STATUS</th><th>ASSIGNEE</th><th>ACTIONS</th></tr></thead><tbody>{filtered.map(t=><tr key={t.ticket_id}><td><div className="table-primary">{t.subject}</div><small className="table-sub">{t.ticket_id.slice(0,8)}…</small></td><td>{t.customer_id}</td><td><span className={`priority ${t.priority}`}>{t.priority}</span></td><td><select className="status-select" value={t.status} onChange={e=>updateStatus(t,e.target.value as Ticket["status"])}><option value="open">Open</option><option value="in_progress">In progress</option><option value="resolved">Resolved</option><option value="closed">Closed</option></select></td><td>{t.assigned_to||"Unassigned"}</td><td><button className="table-action danger" onClick={()=>remove(t)} title="Delete ticket"><X size={16}/></button></td></tr>)}</tbody></table></div>}
    </section>

    {showForm && <div className="modal-backdrop" onClick={()=>setShowForm(false)}><div className="modal" onClick={e=>e.stopPropagation()}><div className="modal-heading"><div><h2>Create support ticket</h2><p>Enter the customer request details.</p></div><button className="icon-button" onClick={()=>setShowForm(false)}><X size={19}/></button></div>
      <form onSubmit={create} className="ticket-form">
        <label>Customer ID<input required value={form.customer_id} onChange={e=>setForm({...form,customer_id:e.target.value})} placeholder="e.g. customer_001"/></label>
        <label>Chat session ID<input required value={form.session_id} onChange={e=>setForm({...form,session_id:e.target.value})} placeholder="Paste conversation session ID"/></label>
        <label>Subject<input required value={form.subject} onChange={e=>setForm({...form,subject:e.target.value})} placeholder="Brief issue summary"/></label>
        <label>Description<textarea required rows={4} value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Describe the customer's issue…"/></label>
        <label>Priority<select value={form.priority} onChange={e=>setForm({...form,priority:e.target.value as Ticket["priority"]})}><option value="low">Low</option><option value="normal">Normal</option><option value="high">High</option><option value="urgent">Urgent</option></select></label>
        <div className="modal-actions"><button type="button" className="button button-secondary" onClick={()=>setShowForm(false)}>Cancel</button><button className="button button-primary" disabled={saving}>{saving?"Creating…":"Create ticket"}</button></div>
      </form>
    </div></div>}
  </div>;
}
