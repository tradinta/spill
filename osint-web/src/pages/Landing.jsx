import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Shield, Globe, Activity, Eye, FileJson } from 'lucide-react';

export default function Landing() {
  const [target, setTarget] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (target) {
      navigate(`/dashboard?target=${encodeURIComponent(target)}`);
    }
  };

  const platforms = [
    { name: 'X / Twitter', icon: <Globe size={24} />, desc: 'Interaction networks & sleep cycles', color: 'blue' },
    { name: 'TikTok', icon: <Activity size={24} />, desc: 'Video metadata & engagement stats', color: 'purple' },
    { name: 'Reddit', icon: <Shield size={24} />, desc: 'Karma breakdowns & writing style', color: 'red' },
    { name: 'Instagram', icon: <Eye size={24} />, desc: 'Visual archives & behavioral profiling', color: 'blue' },
    { name: 'LinkedIn', icon: <FileJson size={24} />, desc: 'Corporate espionage & connections', color: 'purple' },
    { name: 'Facebook', icon: <Globe size={24} />, desc: 'Deep social graph & geo-location', color: 'blue' },
  ];

  return (
    <div className="container">
      {/* Hero Section */}
      <section style={{ padding: '6rem 0', textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
        <div className="badge badge-purple animate-fade-in" style={{ marginBottom: '1.5rem' }}>
          Mission Critical Intelligence V2.0
        </div>
        <h1 className="animate-fade-in stagger-1" style={{ fontSize: '4rem', fontWeight: 800, lineHeight: 1.1, marginBottom: '1.5rem', letterSpacing: '-0.02em' }}>
          Deep Intelligence. <br/>
          <span className="text-gradient">Zero Trace.</span>
        </h1>
        <p className="animate-fade-in stagger-2" style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '3rem' }}>
          Deploy advanced recon across 6 major social networks. Extract behavioral 
          fingerprints, interaction graphs, and metadata instantly.
        </p>

        {/* Interactive Search Bar */}
        <form onSubmit={handleSearch} className="animate-fade-in stagger-3" style={{ position: 'relative', maxWidth: '600px', margin: '0 auto' }}>
          <div className="glass-panel" style={{ display: 'flex', padding: '0.5rem', borderRadius: '12px', alignItems: 'center', background: 'rgba(15, 15, 20, 0.8)' }}>
            <Search size={24} color="var(--text-muted)" style={{ marginLeft: '1rem' }} />
            <input 
              type="text" 
              placeholder="Enter target username (e.g. elonmusk, spez)"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'white',
                padding: '1rem',
                flex: 1,
                fontSize: '1.1rem',
                outline: 'none'
              }}
            />
            <button type="submit" className="btn-primary" style={{ padding: '0.75rem 2rem' }}>
              Deploy
            </button>
          </div>
        </form>
      </section>

      {/* Features Grid */}
      <section style={{ padding: '4rem 0' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Supported Vectors</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Full spectrum analysis across the social web.</p>
        </div>
        
        <div className="grid grid-cols-3">
          {platforms.map((p, i) => (
            <div key={p.name} className={`glass-panel animate-fade-in stagger-${(i%3)+1}`} style={{ padding: '2rem' }}>
              <div className={`badge badge-${p.color}`} style={{ width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', padding: 0 }}>
                {p.icon}
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{p.name}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{p.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
