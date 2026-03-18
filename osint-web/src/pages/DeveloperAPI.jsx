import { Code, Terminal, FileJson } from 'lucide-react';

export default function DeveloperAPI() {
  const codeSnippet = `
import httpx

# Omniscient OSINT API Example - X/Twitter Target
API_KEY = "sk-live-xxxxxxxxxxxxxxxxx"
TARGET = "elonmusk"
PLATFORM = "x"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = httpx.post(
    "https://api.omniscient.osint/v2/intelligence",
    headers=headers,
    json={"platform": PLATFORM, "target": TARGET, "deep_scan": True}
)

dossier = response.json()
print(f"Target Clearance: {dossier['dossier_meta']['clearance_level']}")
print(f"Sleep Cycle Matrix generated: {dossier['behavioral_intelligence'].get('Sleep_Cycle_Matrix')}")
`.trim();

  return (
    <div className="container" style={{ padding: '4rem 0' }}>
      <div className="animate-fade-in" style={{ marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Developer <span className="text-gradient">API</span></h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', maxWidth: '800px' }}>
          Integrate our 6 powerful OSINT scraping engines directly into your applications. 
          Enterprise node required for production keys.
        </p>
      </div>

      <div className="grid grid-cols-3">
        {/* Left Col - Navigation/Docs */}
        <div className="glass-panel animate-fade-in stagger-1" style={{ padding: '2rem' }}>
          <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileJson size={20} color="var(--accent-blue)"/> Endpoints
          </h3>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <li>
              <div className="badge badge-purple" style={{ marginRight: '0.5rem', fontSize: '0.6rem' }}>POST</div>
              <code>/v2/intelligence</code>
            </li>
            <li style={{ color: 'var(--text-secondary)' }}>
              <div className="badge badge-blue" style={{ marginRight: '0.5rem', fontSize: '0.6rem' }}>GET</div>
              <code>/v2/target/status</code>
            </li>
            <li style={{ color: 'var(--text-secondary)' }}>
              <div className="badge badge-blue" style={{ marginRight: '0.5rem', fontSize: '0.6rem' }}>GET</div>
              <code>/v2/network/graph</code>
            </li>
          </ul>

          <div style={{ marginTop: '3rem' }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem', textTransform: 'uppercase' }}>Supported Platforms</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              <span className="badge badge-blue">x</span>
              <span className="badge badge-purple">tiktok</span>
              <span className="badge badge-red">reddit</span>
              <span className="badge badge-blue">instagram</span>
              <span className="badge badge-purple">linkedin</span>
              <span className="badge badge-blue">facebook</span>
            </div>
          </div>
        </div>

        {/* Right Col - Code & Snippets */}
        <div className="glass-panel animate-fade-in stagger-2" style={{ gridColumn: 'span 2', padding: '0', overflow: 'hidden' }}>
          <div style={{ background: 'rgba(0,0,0,0.4)', padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Terminal size={18} color="var(--text-muted)" />
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>example_request.py</span>
          </div>
          <div style={{ padding: '1.5rem' }}>
            <pre style={{ margin: 0, fontFamily: 'var(--font-mono)', fontSize: '0.9rem', overflowX: 'auto', color: '#e2e8f0' }}>
              <code>{codeSnippet}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
