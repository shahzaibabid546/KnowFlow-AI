import { useState } from "react";
import type { FormEvent } from "react";
import { Bot, Check, Copy, MessageSquare, Plus, Send, Sparkles, UserRound } from "lucide-react";
import { apiService, getErrorMessage } from "../api";
import type { ChatMessage } from "../types";

export default function Chat() {
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(-1);

  async function newChat() {
    setError(""); setBusy(true);
    try {
      const session = await apiService.createSession();
      setSessionId(session.session_id);
      setMessages([]);
    } catch (e) { setError(getErrorMessage(e)); }
    finally { setBusy(false); }
  }

  async function send(e: FormEvent) {
    e.preventDefault();
    const question = input.trim();
    if (!question || busy) return;
    setError("");
    setBusy(true);
    let currentId = sessionId;
    try {
      if (!currentId) {
        const session = await apiService.createSession();
        currentId = session.session_id;
        setSessionId(currentId);
      }
      setMessages(prev => [...prev, { role: "user", content: question }]);
      setInput("");
      const result = await apiService.sendMessage(currentId, question);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: result.answer || "The assistant returned an empty response.",
        sources: result.sources || [],
      }]);
      if (result.needs_human) setError(`This conversation was escalated: ${result.escalation_reason || "Human support is required."}`);
    } catch (e) {
      setError(getErrorMessage(e));
      // Keep the user's question visible if the API call fails.
    } finally { setBusy(false); }
  }

  return <div className="page-stack chat-page">
    <section className="page-heading-row"><div><div className="eyebrow"><Sparkles size={14}/> KNOWFLOW AI</div><h1>AI Assistant</h1><p>Ask questions and get answers grounded in your company knowledge.</p></div><button className="button button-secondary" onClick={newChat} disabled={busy}><Plus size={16}/> New chat</button></section>
    <section className="chat-layout panel">
      <div className="chat-main">
        <div className="chat-toolbar"><div className="chat-agent"><div className="agent-avatar"><Bot size={19}/></div><div><strong>KnowFlow Assistant</strong><small><span className="status-dot online"/> AI support agent</small></div></div><div className="session-label">{sessionId ? `Session ${sessionId.slice(0,8)}…` : "New conversation"}</div></div>
        <div className="messages-area">
          {messages.length === 0 ? <div className="chat-empty">
            <div className="chat-empty-icon"><Sparkles size={27}/></div><h2>How can I help you today?</h2><p>Ask about company policies, refunds, services, or anything in your uploaded knowledge base.</p>
            <div className="suggestion-grid">{["What is your refund policy?","How can I contact customer support?","What are your company policies?"].map(q=><button key={q} onClick={()=>setInput(q)}>{q}<span>↗</span></button>)}</div>
          </div> : messages.map((m,i)=><div className={`message-row ${m.role}`} key={`${i}-${m.role}`}><div className={`message-avatar ${m.role}`}>{m.role==="user"?<UserRound size={16}/>:<Bot size={17}/>}</div><div className="message-body"><div className="message-author">{m.role==="user"?"You":"KnowFlow AI"}</div><div className="message-bubble">{m.content}</div>{m.sources && m.sources.length>0 && <div className="sources"><strong>Sources</strong>{m.sources.map(s=><span className="source-chip" key={s}>{s}</span>)}</div>}{m.role==="assistant" && <button className="copy-button" onClick={()=>{navigator.clipboard?.writeText(m.content);setCopied(i);}}>{copied===i?<Check size={13}/>:<Copy size={13}/>} {copied===i?"Copied":"Copy answer"}</button>}</div></div>)}
          {busy && <div className="message-row assistant"><div className="message-avatar assistant"><Bot size={17}/></div><div className="message-body"><div className="message-author">KnowFlow AI</div><div className="typing"><i/><i/><i/></div></div></div>}
        </div>
        {error && <div className="chat-error">{error}</div>}
        <form className="composer" onSubmit={send}><textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send(e);}}} placeholder="Message KnowFlow AI…" rows={2} disabled={busy}/><div className="composer-bottom"><span>AI can make mistakes. Verify important information.</span><button className="send-button" type="submit" disabled={!input.trim()||busy}><Send size={16}/></button></div></form>
      </div>
      <aside className="chat-aside"><div className="aside-card"><div className="aside-icon"><Sparkles size={18}/></div><h3>Grounded answers</h3><p>KnowFlow searches your uploaded documents and uses relevant content to answer.</p></div><div className="aside-card"><h3>Conversation details</h3><div className="detail-line"><span>Status</span><strong>{sessionId?"Active":"Not started"}</strong></div><div className="detail-line"><span>Messages</span><strong>{messages.length}</strong></div><div className="detail-line"><span>Session ID</span><strong className="truncate">{sessionId?sessionId.slice(0,12)+"…":"—"}</strong></div></div><div className="aside-note"><MessageSquare size={16}/><span>Each new chat creates a separate conversation session.</span></div></aside>
    </section>
  </div>;
}
