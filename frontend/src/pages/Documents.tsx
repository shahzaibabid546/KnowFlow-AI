import { useRef, useState } from "react";
import type { ChangeEvent, DragEvent } from "react";
import { FileText, FileUp, File, UploadCloud, X, CheckCircle2, AlertCircle } from "lucide-react";
import { apiService, getErrorMessage } from "../api";

type UploadResult = { filename: string; total_chunks?: number; message?: string };

export default function Documents() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File|null>(null);
  const [dragging, setDragging] = useState(false);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<UploadResult|null>(null);
  const [error, setError] = useState("");

  function choose(f?: File) {
    if (!f) return;
    setResult(null); setError("");
    const ext = f.name.split(".").pop()?.toLowerCase();
    if (!["pdf","txt"].includes(ext || "")) { setError("Only PDF and TXT files are supported."); setFile(null); return; }
    setFile(f);
  }
  function onDrop(e: DragEvent<HTMLDivElement>) { e.preventDefault(); setDragging(false); choose(e.dataTransfer.files?.[0]); }
  async function upload() {
    if (!file) return;
    setBusy(true); setError(""); setResult(null);
    try { setResult(await apiService.uploadDocument(file)); setFile(null); if(inputRef.current) inputRef.current.value=""; }
    catch(e) { setError(getErrorMessage(e)); }
    finally { setBusy(false); }
  }

  return <div className="page-stack">
    <section className="page-heading-row"><div><div className="eyebrow"><FileText size={14}/> COMPANY KNOWLEDGE</div><h1>Knowledge Base</h1><p>Upload your company documents to give the AI assistant trusted information.</p></div><div className="supported-pill"><CheckCircle2 size={15}/> PDF & TXT supported</div></section>
    <section className="documents-grid">
      <div className="panel upload-panel">
        <div className="panel-title-row"><div><h2>Upload documents</h2><p>Choose a file or drag it into the upload area.</p></div><div className="upload-heading-icon"><UploadCloud size={20}/></div></div>
        <div className={`dropzone ${dragging?"dragging":""}`} onDragOver={e=>{e.preventDefault();setDragging(true);}} onDragLeave={()=>setDragging(false)} onDrop={onDrop} onClick={()=>inputRef.current?.click()}>
          <div className="drop-icon"><FileUp size={25}/></div><strong>Drop your file here, or <span>browse</span></strong><small>PDF or TXT · Select one file at a time</small>
          <input ref={inputRef} type="file" accept=".pdf,.txt,application/pdf,text/plain" hidden onChange={(e:ChangeEvent<HTMLInputElement>)=>choose(e.target.files?.[0])}/>
        </div>
        {file && <div className="selected-file"><div className="selected-file-icon"><FileText size={19}/></div><div className="selected-file-copy"><strong>{file.name}</strong><small>{(file.size/1024).toFixed(1)} KB · Ready to upload</small></div><button className="icon-button" onClick={()=>setFile(null)} aria-label="Remove file"><X size={17}/></button></div>}
        {error && <div className="inline-error"><AlertCircle size={16}/>{error}</div>}
        {result && <div className="success-box"><CheckCircle2 size={18}/><div><strong>{result.message || "Document uploaded and ingested successfully."}</strong><small>{result.filename} · {result.total_chunks ?? "—"} chunks created</small></div></div>}
        <button className="button button-primary upload-submit" onClick={upload} disabled={!file||busy}>{busy?"Uploading and processing…":<><UploadCloud size={17}/> Upload & process</>}</button>
      </div>
      <div className="panel document-info">
        <h2>How it works</h2><p className="muted-text">Your documents become searchable knowledge for the AI assistant.</p>
        <div className="process-step"><div className="process-icon"><FileText size={17}/></div><div><strong>1. Upload</strong><small>Add a PDF or plain text file.</small></div></div>
        <div className="process-connector"/>
        <div className="process-step"><div className="process-icon"><File size={17}/></div><div><strong>2. Process & split</strong><small>KnowFlow extracts text and creates smaller chunks.</small></div></div>
        <div className="process-connector"/>
        <div className="process-step"><div className="process-icon"><CheckCircle2 size={17}/></div><div><strong>3. Ask questions</strong><small>The retrieval pipeline finds relevant content for answers.</small></div></div>
        <div className="info-callout"><AlertCircle size={16}/><span>Only upload documents you are authorized to use. Current backend storage is in-memory for indexed chunks.</span></div>
      </div>
    </section>
  </div>;
}
