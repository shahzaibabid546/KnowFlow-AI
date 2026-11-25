import { CheckCircle2, ExternalLink, Info, Server, ShieldCheck, Wifi, XCircle } from "lucide-react";

export default function SettingsPage({backendStatus}:{backendStatus:string}) {
  const base = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
  return <div className="page-stack">
    <section className="page-heading-row"><div><div className="eyebrow"><ShieldCheck size={14}/> WORKSPACE PREFERENCES</div><h1>Settings</h1><p>Application configuration and service connectivity.</p></div></section>
    <section className="settings-grid">
      <div className="panel settings-panel"><div className="settings-section-title"><Server size={18}/><div><h2>Backend connection</h2><p>Connection to your KnowFlow FastAPI service.</p></div></div>
        <div className="setting-row"><div><strong>API base URL</strong><small>{base}</small></div><span className="status-badge neutral">Configured</span></div>
        <div className="setting-row"><div><strong>Health status</strong><small>GET /health</small></div>{backendStatus==="online"?<span className="status-badge resolved"><CheckCircle2 size={13}/> Online</span>:backendStatus==="offline"?<span className="status-badge closed"><XCircle size={13}/> Offline</span>:<span className="status-badge neutral">Checking</span>}</div>
        <div className="setting-row"><div><strong>AI provider</strong><small>Google Gemini (configured in backend)</small></div><span className="status-badge neutral">Backend managed</span></div>
      </div>
      <div className="panel settings-panel"><div className="settings-section-title"><Info size={18}/><div><h2>About KnowFlow AI</h2><p>Knowledge and customer support platform.</p></div></div>
        <div className="about-logo"><div className="brand-mark"><span>✦</span></div><div><strong>KnowFlow AI</strong><small>Version 1.0.0 · Frontend</small></div></div>
        <p className="muted-text">This frontend connects to your existing FastAPI backend. API keys and Gemini credentials stay on the backend and should never be placed in frontend environment variables.</p>
        <a className="external-link" href={`${base}/docs`} target="_blank" rel="noreferrer">Open API documentation <ExternalLink size={14}/></a>
      </div>
    </section>
  </div>;
}
