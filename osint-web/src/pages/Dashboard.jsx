import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ShieldAlert, MapPin, Calendar, Users, Hash, Clock, BarChart2, Activity, MessageSquare } from 'lucide-react';

import elonData from '../mockData/elonmusk.json';
import spezData from '../mockData/spez.json';
import zuckData from '../mockData/zuck.json';

// Minimal mapping of target string to our mock JSONs
const mockDatabases = {
  'elonmusk': elonData,
  'elon': elonData,
  'spez': spezData,
  'u/spez': spezData,
  'zuck': zuckData,
  'mark zuckerberg': zuckData
};

export default function Dashboard() {
  const [searchParams] = useSearchParams();
  const targetQuery = searchParams.get('target') || '';
  
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    // Simulate network delay for API recon
    setLoading(true);
    const timer = setTimeout(() => {
      const targetLower = targetQuery.toLowerCase().trim();
      setData(mockDatabases[targetLower] || null);
      setLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, [targetQuery]);

  if (!targetQuery) {
    return (
      <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Mission Control Offline</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Please enter a target username from the Intelligence Hub to begin reconnaissance.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container" style={{ padding: '8rem 0', textAlign: 'center' }}>
        <div className="animate-fade-in" style={{ display: 'inline-block', position: 'relative' }}>
          <Activity size={48} color="var(--accent-blue)" style={{ animation: 'pulse 1.5s infinite' }} />
        </div>
        <h2 style={{ marginTop: '2rem', fontSize: '1.5rem', color: 'var(--text-secondary)' }}>
          Deploying nodes for <span style={{ color: 'white' }}>{targetQuery}</span>...
        </h2>
        <p style={{ marginTop: '0.5rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-purple)', fontSize: '0.9rem' }}>
          Initializing Deep Scan Protocol
        </p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
        <ShieldAlert size={48} color="var(--accent-red)" style={{ margin: '0 auto 1rem auto' }} />
        <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Target Not Found in Cache</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Simulation only supports: <code style={{ color: 'white' }}>elonmusk</code>, <code style={{ color: 'white' }}>spez</code>, or <code style={{ color: 'white' }}>zuck</code>
        </p>
      </div>
    );
  }

  // Define some safe accessors across our varied JSON structures
  const meta = data.dossier_meta || {};
  const arch = data.account_archeology || {};
  const bi = data.behavioral_intelligence || {};
  const platform = meta.target && meta.target.includes('reddit') ? 'Reddit' 
                 : meta.target && meta.target.includes('fb') ? 'Facebook' 
                 : 'X / Twitter';

  return (
    <div className="container" style={{ padding: '2rem 0' }}>
      {/* Target Header */}
      <div className="glass-panel animate-fade-in" style={{ padding: '2rem', marginBottom: '2rem', display: 'flex', gap: '2rem', alignItems: 'center' }}>
        {arch.Profile_Image && arch.Profile_Image !== 'N/A' ? (
          <img src={arch.Profile_Image} alt="Profile" style={{ width: '120px', height: '120px', borderRadius: '50%', border: '2px solid var(--accent-blue)', objectFit: 'cover' }} />
        ) : (
          <div style={{ width: '120px', height: '120px', borderRadius: '50%', background: 'var(--bg-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '2px solid var(--accent-blue)' }}>
            <Users size={48} color="rgba(255,255,255,0.2)" />
          </div>
        )}
        
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '0.5rem' }}>
            <h1 style={{ fontSize: '2.5rem', margin: 0, lineHeight: 1 }}>{arch.Full_Name || targetQuery}</h1>
            <span className={`badge ${platform === 'Reddit' ? 'badge-red' : platform === 'Facebook' ? 'badge-blue' : 'badge-purple'}`}>
              {platform} Source
            </span>
            <span className="badge badge-red">{meta.clearance_level || 'CONFIDENTIAL'}</span>
          </div>
          
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginBottom: '1rem', maxWidth: '800px' }}>
            {arch.Description || arch.Biography || data.about_intelligence?.Description || 'No biography available.'}
          </p>
          
          <div style={{ display: 'flex', gap: '1.5rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            {(arch.Location || data.about_intelligence?.Location) && (
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <MapPin size={16} /> {arch.Location || data.about_intelligence.Location}
              </span>
            )}
            {arch.Account_Created && (
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Calendar size={16} /> Created: {arch.Account_Created}
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3">
        {/* Left Column - Metrics & Network */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-panel animate-fade-in stagger-1" style={{ padding: '1.5rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
              <BarChart2 size={18} color="var(--accent-blue)" /> Key Metrics
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {data.public_metrics && Object.entries(data.public_metrics).map(([key, val]) => (
                <div key={key} style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>{key.replace(/_/g, ' ')}</span>
                  <span style={{ fontWeight: 600, fontFamily: 'var(--font-mono)' }}>{val}</span>
                </div>
              ))}
              {data.karma_breakdown && Object.entries(data.karma_breakdown).map(([key, val]) => (
                <div key={key} style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>{key.replace(/_/g, ' ')}</span>
                  <span style={{ fontWeight: 600, fontFamily: 'var(--font-mono)', color: 'var(--accent-red)' }}>{val}</span>
                </div>
              ))}
              {data.about_intelligence && data.about_intelligence.Work && data.about_intelligence.Work !== 'N/A' && (
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Work</span>
                  <span style={{ fontWeight: 600, textAlign: 'right' }}>{data.about_intelligence.Work[0]}</span>
                </div>
              )}
            </div>
          </div>

          {(data.interaction_network || bi.Interaction_Network) && (
             <div className="glass-panel animate-fade-in stagger-2" style={{ padding: '1.5rem' }}>
               <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                 <Users size={18} color="var(--accent-purple)" /> Interaction Graph
               </h3>
               {Object.entries(data.interaction_network?.Top_Replying_To || bi.Interaction_Network?.Top_Replying_To || {}).map(([user, count]) => (
                 <div key={user} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                   <span style={{ color: 'var(--text-secondary)' }}>@{user}</span>
                   <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-blue)' }}>{count} interactions</span>
                 </div>
               ))}
             </div>
          )}
        </div>

        {/* Middle/Right Column - Deep Intel & Sleep Cycles */}
        <div style={{ gridColumn: 'span 2', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {(bi.Sleep_Cycle_Matrix || bi.Activity_Heatmap) && (
            <div className="glass-panel animate-fade-in stagger-1" style={{ padding: '1.5rem' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                <Clock size={18} color="var(--accent-green)" /> Behavioral Heatmap (UTC)
              </h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                {Object.entries(bi.Sleep_Cycle_Matrix || bi.Activity_Heatmap).map(([hour, count]) => {
                  const intensity = Math.min((count / 10), 1);
                  return (
                    <div 
                      key={hour}
                      title={`Hour ${hour}: ${count} actions`}
                      style={{
                        width: '32px', height: '32px',
                        background: count === 0 ? 'rgba(255,255,255,0.05)' : `rgba(0, 240, 255, ${0.2 + (intensity * 0.8)})`,
                        borderRadius: '4px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '0.7rem', color: count > 3 ? '#000' : 'var(--text-muted)'
                      }}
                    >
                      {hour}
                    </div>
                  );
                })}
              </div>
              <p style={{ marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Identified Peak Hour: {bi.Peak_Activity_Hour || 'Unknown'} | Inferred Timezone constraint applied.
              </p>
            </div>
          )}

          <div className="grid grid-cols-2" style={{ gap: '1.5rem' }}>
            {data.writing_style_analysis && (
              <div className="glass-panel animate-fade-in stagger-2" style={{ padding: '1.5rem' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                  <MessageSquare size={18} color="var(--accent-purple)" /> Linguistic Fingerprint
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Avg Word Count</span>
                    <span style={{ fontFamily: 'var(--font-mono)' }}>{data.writing_style_analysis.Avg_Words_Per_Post}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Vocabulary Size</span>
                    <span style={{ fontFamily: 'var(--font-mono)' }}>{data.writing_style_analysis.Unique_Words_Used}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>Sentiment Index</span>
                    <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-green)' }}>
                      {(data.writing_style_analysis.Positive_Sentiment_Ratio * 100).toFixed(1)}% Positive
                    </span>
                  </div>
                </div>
              </div>
            )}

            {(bi.Top_Hashtags || data.top_posts || data.visible_posts || bi.Top_Subreddits) && (
              <div className="glass-panel animate-fade-in stagger-3" style={{ padding: '1.5rem' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                  <Hash size={18} color="var(--accent-blue)" /> Topical Affinity
                </h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {(bi.Top_Hashtags || bi.Top_Subreddits || Object.keys(data.behavioral_intelligence?.Subreddit_Affinity || {})).slice(0, 10).map((tag, i) => (
                    <span key={i} className="badge badge-blue">
                      {typeof tag === 'string' ? tag : tag[0]} {/* Handles arrays or tuple chunks */}
                    </span>
                  ))}
                  {data.visible_posts && data.visible_posts.slice(0,2).map((post, i) => (
                    <p key={i} style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontStyle: 'italic', marginBottom: '0.5rem', borderLeft: '2px solid var(--border-color)', paddingLeft: '0.5rem' }}>
                      "{post.substring(0, 100)}..."
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
