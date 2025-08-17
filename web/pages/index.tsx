import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

export default function Home() {
  const [progress, setProgress] = useState(0);
  async function onDrop(e: React.DragEvent) {
    e.preventDefault();
    const files = e.dataTransfer.files;
    for (const f of Array.from(files)) {
      const init = await fetch(`${API}/uploads/init`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
        name: f.name,
        size: f.size,
        contentType: f.type
      })
      }).then(r=>r.json());

      const partSize = init.partSize;
      const parts:any[] = [];
      await Promise.all(init.parts.map(async (p:any) => {
        const start = (p.partNumber-1)*partSize;
        const end   = Math.min(start+partSize, f.size);
        const blob  = f.slice(start,end);
        const resp  = await fetch(p.url, { method:"PUT", body: blob });
        if (!resp.ok) throw new Error("part failed");
        const etag = resp.headers.get("ETag")?.replaceAll('"','') || "";
        parts.push({ partNumber: p.partNumber, etag });
        setProgress(prev => Math.min(100, prev + (blob.size / f.size) * 100));
      }));

      await fetch(`${API}/uploads/complete`, {
        method:"POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uploadId: init.uploadId, key: init.key, parts })
      });
    }
  }

  return (
    <div style={{maxWidth: 720, margin: "40px auto", fontFamily: "system-ui"}}>
      <h1>Drive (Local)</h1>
      <div onDrop={onDrop} onDragOver={(e)=>e.preventDefault()}
           style={{border: "2px dashed #999", padding: 40, textAlign: "center", borderRadius: 8}}>
        <p>Drag & drop files here</p>
        <progress value={progress} max={100} style={{width:"100%"}} />
      </div>
      <p style={{marginTop: 16, color: "#666"}}>This local build uses MinIO + Postgres + FastAPI.</p>
    </div>
  );
}
