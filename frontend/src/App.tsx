import { useEffect, useState } from "react";
import { NavLink, Route, Routes, useLocation } from "react-router-dom";
import {
  Activity, BookOpen, Bot, CheckCircle2, ChevronDown, CircleHelp,
  FileText, LayoutDashboard, Menu, MessageSquare, Settings, ShieldCheck,
  Ticket as TicketIcon, Wifi, X
} from "lucide-react";
import { apiService, getErrorMessage } from "./api";
import Overview from "./pages/Overview";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
import Tickets from "./pages/Tickets";
import SettingsPage from "./pages/SettingsPage";

const navItems = [
  { to: "/", label: "Overview", icon: LayoutDashboard, end: true },
  { to: "/chat", label: "AI Assistant", icon: MessageSquare },
  { to: "/documents", label: "Knowledge Base", icon: BookOpen },
  { to: "/tickets", label: "Support Tickets", icon: TicketIcon },
  { to: "/settings", label: "Settings", icon: Settings },
];

function titleFor(path: string) {
  if (path.startsWith("/chat")) return "AI Assistant";
  if (path.startsWith("/documents")) return "Knowledge Base";
  if (path.startsWith("/tickets")) return "Support Tickets";
  if (path.startsWith("/settings")) return "Settings";
  return "Overview";
}

export default function App() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");

  useEffect(() => {
    let active = true;
    const check = async () => {
      try {
        await apiService.health();
        if (active) setBackendStatus("online");
      } catch {
        if (active) setBackendStatus("offline");
      }
    };
    check();
    const timer = window.setInterval(check, 30000);
    return () => { active = false; window.clearInterval(timer); };
  }, []);

  useEffect(() => setMobileOpen(false), [location.pathname]);

  return (
    <div className="app-shell">
      {mobileOpen && <button className="mobile-scrim" aria-label="Close navigation" onClick={() => setMobileOpen(false)} />}
      <aside className={`sidebar ${mobileOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><Bot size={23} /></div>
          <div><strong>KnowFlow<span>AI</span></strong><small>KNOWLEDGE WORKSPACE</small></div>
          <button className="icon-button mobile-close" onClick={() => setMobileOpen(false)} aria-label="Close menu"><X size={18}/></button>
        </div>

        <div className="workspace-switch">
          <div className="workspace-avatar">K</div>
          <div className="workspace-copy"><strong>Acme Workspace</strong><small>Single workspace</small></div>
          <ChevronDown size={15} className="muted"/>
        </div>

        <div className="nav-caption">WORKSPACE</div>
        <nav className="main-nav">
          {navItems.map(({to,label,icon:Icon,end}) => (
            <NavLink key={to} to={to} end={end} className={({isActive}) => `nav-link ${isActive ? "active" : ""}`}>
              <Icon size={18}/><span>{label}</span>
              {label === "Support Tickets" && <span className="nav-dot"/>}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-icon"><CircleHelp size={17}/></div>
            <strong>Need a hand?</strong>
            <p>Your knowledge assistant is ready to help.</p>
            <NavLink to="/chat">Open AI assistant <span>↗</span></NavLink>
          </div>
          <div className="profile-row">
            <div className="profile-avatar">A</div>
            <div className="profile-copy"><strong>Admin User</strong><small>Workspace admin</small></div>
            <Settings size={16} className="muted"/>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <button className="icon-button menu-toggle" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><Menu size={20}/></button>
            <div className="breadcrumb">Workspace <span>/</span> <strong>{titleFor(location.pathname)}</strong></div>
          </div>
          <div className="topbar-right">
            <div className={`connection-pill ${backendStatus}`}><span className="status-dot"/>{backendStatus === "checking" ? "Checking API" : backendStatus === "online" ? "Backend connected" : "Backend offline"}</div>
            <div className="topbar-divider"/>
            <div className="top-avatar">A</div>
          </div>
        </header>
        {backendStatus === "offline" && (
          <div className="offline-banner"><Wifi size={16}/> Backend connection unavailable. Start your FastAPI server at <code>127.0.0.1:8000</code> to use live features.</div>
        )}
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Overview backendStatus={backendStatus}/>}/>
            <Route path="/chat" element={<Chat/>}/>
            <Route path="/documents" element={<Documents/>}/>
            <Route path="/tickets" element={<Tickets/>}/>
            <Route path="/settings" element={<SettingsPage backendStatus={backendStatus}/>}/>
            <Route path="*" element={<Overview backendStatus={backendStatus}/>}/>
          </Routes>
        </div>
        <footer className="footer"><span>© 2026 KnowFlow AI</span><span><ShieldCheck size={13}/> Your knowledge, connected.</span></footer>
      </main>
    </div>
  );
}
