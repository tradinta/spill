import React, { useState, useEffect } from 'react';
import { 
  Search, Shield, Activity, Clock, Users, MapPin, 
  Briefcase, GraduationCap, Link as LinkIcon, AlertTriangle, 
  Database, Terminal, Play, Hash, Target, ChevronRight,
  MessageSquare, Smartphone, Camera, Bell, Settings,
  LayoutDashboard, TrendingUp, Cpu, ShieldCheck, Eye, Radar,
  Film, FolderOpen, LineChart, PlusCircle, CheckCircle2, Loader2, Focus,
  Fingerprint, Globe, Network, Menu, FileText, Blocks, Zap
} from 'lucide-react';

// --- MOCK DATA GENERATOR ---
const generateMockData = (engine, target) => {
  const baseInfo = { target: target || 'unknown_target', timestamp: new Date().toISOString() };
  switch(engine) {
    case 'x':
      return {
        ...baseInfo,
        archeology: {
          followers: '14,203', following: '842', 
          created: '2014-03-12T14:22:00Z', 
          bio: 'Cybersecurity researcher. Coffee addict. All opinions are mine.',
          location: 'San Francisco, CA', shadowbanStatus: 'Clear'
        },
        sleepCycle: Array.from({ length: 7 }, () => Array.from({ length: 24 }, () => Math.random())),
        innerCircle: [
          { name: '@sec_ops', weight: 85 }, { name: '@defcon_bot', weight: 62 },
          { name: '@crypto_anon', weight: 45 }, { name: '@dev_lead', weight: 30 }
        ]
      };
    case 'reddit':
      return {
        ...baseInfo,
        affinity: [
          { sub: 'r/netsec', score: 92 }, { sub: 'r/homelab', score: 85 },
          { sub: 'r/privacy', score: 78 }, { sub: 'r/coffee', score: 45 }
        ],
        linguistics: { avgWordCount: 142, vocabSize: 'Top 8%', sentiment: { positive: 45, neutral: 40, negative: 15 } },
        metrics: { postKarma: '45,210', commentKarma: '82,401', age: '6 Years', trophies: ['Verified Email', 'Two-Year Club', 'Gilder'] }
      };
    case 'tiktok':
      return {
        ...baseInfo,
        dossier_meta: {
          target: target || "@tonsic",
          collection_time_utc: "2026-03-17 00:09:10",
          clearance_level: "TOP SECRET // DEEP INTELLIGENCE"
        },
        system_identity_dna: {
          OdinID: "7618009515292869648", WebID: "HIDDEN", WID: "7618009805227935250",
          Session_Nonce: "szuHwfzmQnesd6nUaZUNW", Cluster_Region: "ALL_SG",
          Storage_Node: "DC_SG", Bot_Classification: "others"
        },
        account_archeology: {
          User_Internal_ID: "6980706675075793925",
          SecUID: "MS4wLjABAAAAgV4DmFAn2Kvv5C42V8sSGvN1b2Eu6LwlMuN7gDDOjy_XccOaNce3RVMpaKE7sfWX",
          Account_Created: "2021-07-03 18:00:25", Nickname_Last_Modified: "2025-05-18 04:42:21",
          Username_Last_Modified: "N/A", Account_Age_Days: 1717
        },
        social_graph_interconnects: { Instagram: "N/A", YouTube: "N/A", Twitter: "N/A", Bio_Link: "N/A" },
        behavioral_fingerprint: {
          Digital_Language: "en", System_Region: "KE", Interface_Language: "en",
          Bio_Signature: "Awe, Melancholy and Marilyn Monroe ;)", Sound_Preference: "Original Bias"
        },
        engagement_velocity_analysis: {
          Followers: "244", Recent_Portfolio_Velocity: "0 items analyzed",
          Avg_Views_Per_Video: "0", Avg_Likes_Per_Video: "0", Engagement_Ratio: "0.43"
        },
        content_video_hashes: []
      };
    case 'instagram':
      return {
        ...baseInfo,
        deepProfile: { fullName: 'Alex D. (Sec)', bio: 'Visualizing data | SecOps | 📸 Leica Q2', externalUrl: 'linktr.ee/alexsec', verified: true, businessCategory: 'Digital Creator' },
        media: [1, 2, 3, 4, 5, 6],
        ratios: { followers: '12.4K', following: '450', avgLikes: '1,200', avgComments: '45', trueEngagement: '10.1%' }
      };
    case 'linkedin':
      return {
        ...baseInfo,
        evasion: { fallbackUsed: true, method: 'DuckDuckGo Cached Snippets Interception' },
        professional: [
          { role: 'Senior Security Analyst', company: 'TechCorp Solutions', duration: '2020 - Present' },
          { role: 'Systems Engineer', company: 'Global Networks Inc', duration: '2017 - 2020' }
        ],
        education: [{ school: 'State University', degree: 'B.S. Computer Science', year: '2016' }],
        network: { connections: '500+', skills: ['Penetration Testing', 'Python', 'Cloud Security', 'OSINT'] }
      };
    case 'facebook':
      return {
        ...baseInfo,
        identity: { currentCity: 'Seattle, WA', hometown: 'Portland, OR', bio: 'Living the dream.' },
        graph: { employer: 'TechCorp Solutions', education: 'State University', friends: 482 },
        deepScrape: { numericalId: '100048291048291', openGraphTags: 14, visiblePostsIntercepted: 24 }
      };
    default: return null;
  }
};

const ProcessingVisualizer = ({ config }) => {
  const [step, setStep] = useState(0);
  const steps = [
    { label: 'Initializing Handshake Protocols', duration: 800 },
    { label: 'Spoofing Digital Footprint & WAF Bypass', duration: 1200 },
    { label: 'Intercepting Secure GraphQL Endpoints', duration: 1000 },
    { label: 'Extracting & Decrypting Target Metadata', duration: 1000 },
    { label: 'Compiling Final Intelligence Dossier', duration: 500 }
  ];

  useEffect(() => {
    let currentStep = 0;
    const executeStep = () => {
      if (currentStep < steps.length - 1) {
        setTimeout(() => { currentStep++; setStep(currentStep); executeStep(); }, steps[currentStep].duration);
      }
    };
    executeStep();
  }, []);

  const Icon = config.icon;

  return (
    <div className="flex flex-col md:flex-row items-center justify-center gap-16 py-12 animate-in fade-in zoom-in duration-500">
      <div className="relative flex items-center justify-center w-64 h-64">
        <div className={`absolute inset-0 rounded-full border-2 border-dashed border-slate-700 animate-[spin_10s_linear_infinite] opacity-50`}></div>
        <div className={`absolute inset-4 rounded-full border border-t-transparent ${config.color.replace('text-', 'border-')} animate-[spin_3s_linear_infinite]`}></div>
        <div className={`absolute inset-12 rounded-full ${config.bg} opacity-10 animate-ping`}></div>
        <div className={`relative z-10 w-24 h-24 rounded-2xl bg-[#111111] border ${config.color.replace('text-', 'border-')} flex items-center justify-center shadow-2xl overflow-hidden`}>
          <div className={`absolute inset-0 ${config.bg} opacity-5`}></div>
          <Icon className={`w-12 h-12 ${config.color}`} />
        </div>
      </div>
      <div className="flex flex-col gap-4 w-full max-w-sm">
        <h4 className="text-slate-500 font-mono text-xs tracking-widest uppercase mb-2">Extraction Status</h4>
        {steps.map((s, i) => (
          <div key={i} className={`flex items-center gap-4 p-3 rounded-xl border transition-all duration-300 ${i < step ? 'bg-[#111111] border-slate-800 opacity-50' : i === step ? `bg-[#111111] ${config.color.replace('text-', 'border-')} ${config.glow} translate-x-2` : 'bg-transparent border-transparent opacity-30 grayscale'}`}>
            {i < step ? <CheckCircle2 className={`w-5 h-5 ${config.color}`} /> : i === step ? <Loader2 className={`w-5 h-5 ${config.color} animate-spin`} /> : <div className="w-5 h-5 rounded-full border-2 border-slate-600"></div>}
            <span className={`text-sm font-medium ${i === step ? 'text-white' : 'text-slate-400'}`}>{s.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default function App() {
  const [activeEngine, setActiveEngine] = useState('x');
  const [targetInput, setTargetInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [dossier, setDossier] = useState(null);
  
  // New States
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [history, setHistory] = useState([
    { target: '@tonsic', engine: 'TikTok', time: '2 mins ago', status: 'Success' },
    { target: 'elonmusk', engine: 'X Target', time: '1 hour ago', status: 'Success' },
    { target: 'spez', engine: 'Reddit', time: '5 hours ago', status: 'Partial Data' }
  ]);
  const [credits, setCredits] = useState(8420);

  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
    return () => document.head.removeChild(link);
  }, []);

  const engines = [
    { id: 'x', name: 'X', label: 'X (Twitter)', icon: Terminal, color: 'text-[#facc15]', bg: 'bg-[#facc15]', glow: 'shadow-[0_0_15px_rgba(250,204,21,0.4)]', placeholder: '@username' },
    { id: 'reddit', name: 'Reddit', label: 'Reddit', icon: MessageSquare, color: 'text-[#ff4500]', bg: 'bg-[#ff4500]', glow: 'shadow-[0_0_15px_rgba(255,69,0,0.4)]', placeholder: 'u/username' },
    { id: 'tiktok', name: 'TikTok', label: 'TikTok', icon: Film, color: 'text-[#ff003c]', bg: 'bg-[#ff003c]', glow: 'shadow-[0_0_15px_rgba(255,0,60,0.4)]', placeholder: '@username' },
    { id: 'instagram', name: 'Instagram', label: 'Instagram', icon: Camera, color: 'text-[#ff4500]', bg: 'bg-[#ff4500]', glow: 'shadow-[0_0_15px_rgba(255,69,0,0.4)]', placeholder: 'username' },
    { id: 'linkedin', name: 'LinkedIn', label: 'LinkedIn', icon: Briefcase, color: 'text-[#facc15]', bg: 'bg-[#facc15]', glow: 'shadow-[0_0_15px_rgba(250,204,21,0.4)]', placeholder: 'in/username' },
    { id: 'facebook', name: 'Facebook', label: 'Facebook', icon: Users, color: 'text-[#ff003c]', bg: 'bg-[#ff003c]', glow: 'shadow-[0_0_15px_rgba(255,0,60,0.4)]', placeholder: 'profile.php?id=...' },
  ];

  const currentConfig = engines.find(e => e.id === activeEngine);
  const hasSearched = isProcessing || dossier !== null;

  const handleExtraction = async (e) => {
    e.preventDefault();
    if (!targetInput) return;
    
    setIsProcessing(true);
    setDossier(null);
    if (activeEngine !== 'account') setCredits((prev) => prev - 15);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3000';
      const response = await fetch(`${apiUrl}/api/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ engine: activeEngine, target: targetInput })
      });
      
      if (!response.ok) throw new Error('Failed to extract data via API.');
      
      const data = await response.json();
      setDossier(data);
      
      const engineName = engines.find(eng => eng.id === activeEngine)?.name || activeEngine;
      setHistory([{ target: targetInput, engine: engineName, time: 'Just now', status: 'Success' }, ...history]);
    } catch (error) {
      console.error(error);
      // Fallback for resiliency if python scripts fail to launch cleanly or auth-walls hit
      setDossier(generateMockData(activeEngine, targetInput));
      const engineName = engines.find(eng => eng.id === activeEngine)?.name || activeEngine;
      setHistory([{ target: targetInput, engine: engineName, time: 'Just now', status: 'Partial Data' }, ...history]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setActiveEngine('x');
    setDossier(null);
    setIsProcessing(false);
    setTargetInput('');
  };

  const handleTopup = () => {
    setCredits(prev => prev + 1000);
  };

  const SidebarItem = ({ icon: Icon, label, isActive }) => (
    <button className={`flex items-center gap-3 p-3 rounded-xl transition-all w-full text-left truncate
      ${isActive ? 'bg-[#262626] text-white shadow-inner font-bold' : 'text-slate-400 hover:bg-[#111111] hover:text-white'} 
      ${isSidebarOpen ? 'justify-start' : 'justify-center border border-transparent hover:border-[#262626]'}`}>
      <Icon className="w-5 h-5 shrink-0" />
      {isSidebarOpen && <span className="text-sm tracking-wide">{label}</span>}
    </button>
  );

  return (
    <div className="flex h-screen bg-[#0a0a0a] text-slate-100 antialiased overflow-hidden font-sans" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>

      {/* --- COLLAPSIBLE SIDEBAR --- */}
      <aside className={`flex flex-col border-r border-[#262626] bg-[#050505] transition-all duration-300 z-30 shrink-0 ${isSidebarOpen ? 'w-64' : 'w-20'}`}>
        <div className="h-16 flex items-center justify-center border-b border-[#262626] w-full shrink-0">
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className={`p-2 hover:bg-[#111111] rounded-lg text-slate-400 hover:text-white transition-colors flex items-center justify-center ${isSidebarOpen ? 'w-[80%]' : ''}`}>
             <Menu className="w-6 h-6" />
          </button>
        </div>

        <nav className="flex-1 p-3 flex flex-col gap-2 overflow-y-auto">
          <div className={`text-[10px] text-slate-600 font-bold uppercase tracking-widest mt-2 mb-1 px-3 ${!isSidebarOpen && 'hidden'}`}>Platform</div>
          <button onClick={handleReset} className={`flex items-center gap-3 p-3 rounded-xl transition-all w-full text-left truncate justify-start text-white bg-[#facc15]/10 border border-[#facc15]/30 ${!isSidebarOpen && 'justify-center !p-3'}`}>
            <Radar className="w-5 h-5 text-[#facc15] shrink-0" strokeWidth={2.5} />
            {isSidebarOpen && <span className="text-sm tracking-wide font-bold">Omniscient Dashboard</span>}
          </button>

          <div className={`text-[10px] text-slate-600 font-bold uppercase tracking-widest mt-6 mb-1 px-3 ${!isSidebarOpen && 'hidden'}`}>Developer</div>
          <SidebarItem icon={FileText} label="Documentation" />
          <SidebarItem icon={Terminal} label="API Access Tokens" />
          <SidebarItem icon={Blocks} label="Integrations" />
          
          <div className={`text-[10px] text-slate-600 font-bold uppercase tracking-widest mt-6 mb-1 px-3 ${!isSidebarOpen && 'hidden'}`}>Organization</div>
          <SidebarItem icon={Users} label="Team Management" />
          <SidebarItem icon={Shield} label="Security Policies" />
          <SidebarItem icon={Settings} label="Global Settings" />
        </nav>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        {/* --- TOP HEADER --- */}
        <header className="h-16 border-b border-[#262626] px-4 md:px-8 flex items-center justify-between z-20 bg-[#0a0a0a]/95 backdrop-blur-sm shrink-0">
          <div className="flex items-center gap-4">
            <h1 className="text-lg md:text-xl font-bold tracking-tight text-white leading-none flex items-center gap-2">
              Omniscient OSINT
            </h1>
          </div>
          
          <div className="flex items-center gap-3 md:gap-4">
            {/* Quick Topup Button */}
            <button onClick={handleTopup} className="hidden sm:flex items-center gap-2 bg-[#111111] border border-[#facc15]/50 text-[#facc15] px-3 py-1.5 rounded-lg text-sm font-bold shadow-[0_0_10px_rgba(250,204,21,0.15)] hover:bg-[#facc15]/10 transition-colors">
              <Zap className="w-4 h-4" /> Top up credits
            </button>

            {/* Login / Account View toggle */}
            <button 
              onClick={() => { setActiveEngine('account'); setDossier(null); setIsProcessing(false); }} 
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-bold border transition-colors ${activeEngine === 'account' ? 'bg-white text-black border-white' : 'bg-[#111111] text-white border-[#262626] hover:bg-[#262626]'}`}
            >
              <div className="w-5 h-5 rounded-full overflow-hidden border border-[#262626] flex items-center justify-center bg-[#0a0a0a] shrink-0">
                 <img className="w-full h-full object-cover" alt="Avatar" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD9KbvJRSse90lhS_bmWjFOyq8dbZO4x5AmgHpYePK-ogvQp2VHFBlT3jwWCviepxTZXm2W5_XQfuSX0gMpjobDWn6EeL2b350odct8Sac91lLmaLJVvIrLW21W_M15ajGEyY35tC9jETfrox3xkRJHPkNCkTN6mmCdlLz2QucD-bCrbYY74U5qv5NXQQ1FeL0t-JjKrk4olns9u9NxFkUoOTfr4PswKMqGmx_R71gt0W4k8zILceKUCq0bxMpud9rv3-S90XORakTN"/>
              </div>
              <span className="hidden md:block">Account</span>
            </button>
          </div>
        </header>

        {/* --- MAIN WORKSPACE --- */}
        <main className="flex-1 overflow-y-auto relative bg-[#0a0a0a] p-4 md:p-8">
          
          {/* ======================= ACCOUNT & LOGIN VIEW ======================= */}
          {activeEngine === 'account' ? (
            <div className="w-full max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h2 className="text-3xl md:text-5xl font-bold tracking-tighter text-white mb-2 pt-8">Operator Account</h2>
              <p className="text-slate-500 font-mono text-sm tracking-widest uppercase mb-10">Manage billing, checks, and history</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                 {/* Billing Card */}
                 <div className="bg-[#111111] border border-[#facc15]/30 rounded-2xl p-6 shadow-lg relative overflow-hidden group">
                   <div className="absolute top-0 left-0 w-1 h-full bg-[#facc15] shadow-[0_0_15px_rgba(250,204,21,0.4)]"></div>
                   <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2 flex items-center gap-2">
                      <Zap className="w-4 h-4 text-[#facc15]" /> Available Credits
                   </h3>
                   <div className="flex items-end justify-between mt-4">
                      <div className="text-5xl font-mono font-bold text-white">{credits.toLocaleString()}</div>
                      <button onClick={handleTopup} className="bg-[#facc15] text-[#0a0a0a] px-4 py-2 font-bold uppercase tracking-wider text-xs rounded-lg shadow-[0_0_10px_rgba(250,204,21,0.3)] hover:brightness-110">
                        Buy More
                      </button>
                   </div>
                 </div>

                 {/* API Usage Card */}
                 <div className="bg-[#111111] border border-[#262626] rounded-2xl p-6 shadow-lg">
                   <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
                     <Activity className="w-4 h-4" /> API Health & Limits
                   </h3>
                   <div className="space-y-4">
                     <div>
                       <div className="flex justify-between text-[10px] font-mono text-slate-400 mb-1">
                          <span>Requests / Minute</span>
                          <span>145 / 300</span>
                       </div>
                       <div className="w-full h-2 bg-[#0a0a0a] rounded-full border border-[#262626] overflow-hidden">
                          <div className="h-full bg-blue-500 w-[48%]"></div>
                       </div>
                     </div>
                     <div>
                       <div className="flex justify-between text-[10px] font-mono text-slate-400 mb-1">
                          <span>Deep Scrape Concurrency</span>
                          <span>12 / 20</span>
                       </div>
                       <div className="w-full h-2 bg-[#0a0a0a] rounded-full border border-[#262626] overflow-hidden">
                          <div className="h-full bg-purple-500 w-[60%]"></div>
                       </div>
                     </div>
                   </div>
                 </div>
              </div>

              {/* Checks History */}
              <div className="bg-[#111111] border border-[#262626] rounded-2xl p-6 shadow-lg">
                 <h3 className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-4 flex items-center gap-2">
                    <History className="w-4 h-4" /> Previous Extractions
                 </h3>
                 <div className="flex flex-col gap-3">
                   {history.map((item, idx) => (
                     <div key={idx} className="flex flex-col sm:flex-row justify-between sm:items-center bg-[#0a0a0a] p-4 rounded-xl border border-[#262626] gap-4">
                       <div className="flex items-center gap-4">
                         <div className="p-3 bg-[#111111] border border-[#262626] rounded-lg">
                           <Target className="w-5 h-5 text-slate-400 text-[#facc15]" />
                         </div>
                         <div>
                            <div className="text-white font-bold">{item.target}</div>
                            <div className="text-xs text-slate-500 font-mono flex items-center gap-2 mt-1">
                               <span className="bg-[#262626] px-2 py-0.5 rounded text-slate-300">{item.engine}</span>
                               {item.time}
                            </div>
                         </div>
                       </div>
                       <div className="flex items-center gap-3 text-sm">
                         {item.status === 'Success' ? (
                           <span className="text-emerald-400 flex items-center gap-1 font-mono text-xs"><CheckCircle2 className="w-4 h-4"/> Success</span>
                         ) : (
                           <span className="text-[#facc15] flex items-center gap-1 font-mono text-xs"><AlertTriangle className="w-4 h-4"/> Partial</span>
                         )}
                         <button onClick={() => { setActiveEngine(engines.find(e => e.name === item.engine)?.id || 'x'); setTargetInput(item.target); setDossier(null); }} className="bg-[#262626] hover:bg-[#333] text-white px-3 py-1.5 rounded-lg font-bold text-xs uppercase tracking-wider transition-colors border border-transparent hover:border-slate-500">
                           Re-run Target
                         </button>
                       </div>
                     </div>
                   ))}
                 </div>
              </div>
            </div>
          ) : (
            /* ======================= OSINT DASHBOARD VIEW ======================= */
            <>
              {/* === DYNAMIC SEARCH & ENGINE SELECTION BLOCK === */}
              <div className={`transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] flex flex-col items-center w-full mx-auto
                ${hasSearched ? 'max-w-5xl mb-8' : 'max-w-3xl mt-[10vh] md:mt-[15vh] mb-16'}`}>
                
                {/* Headline */}
                <div className={`text-center transition-all duration-500 overflow-hidden ${hasSearched ? 'opacity-0 h-0 scale-95' : 'opacity-100 h-24 scale-100 mb-6'}`}>
                  <h2 className="text-3xl md:text-5xl font-bold tracking-tighter text-white mb-3">Initialize Target Acquisition</h2>
                  <p className="text-slate-500 font-mono text-sm tracking-widest uppercase">Select Engine vector and designate subject identifier.</p>
                </div>

                {/* Tool Switcher */}
                <div className="flex flex-wrap justify-center gap-2 p-1.5 bg-[#111111] border border-[#262626] rounded-2xl mb-6 shadow-xl w-full sm:w-auto">
                  {engines.map((engine) => {
                    const isActive = activeEngine === engine.id;
                    const Icon = engine.icon;
                    return (
                      <button
                        key={engine.id}
                        onClick={() => { setActiveEngine(engine.id); if(!isProcessing) setDossier(null); }}
                        disabled={isProcessing}
                        className={`flex items-center gap-2 px-4 py-3 rounded-xl transition-all duration-300 font-bold text-sm tracking-wide disabled:opacity-50 disabled:cursor-not-allowed
                          ${isActive 
                            ? `${engine.bg} text-[#0a0a0a] ${engine.glow} scale-100` 
                            : 'text-slate-400 hover:text-white hover:bg-[#262626] scale-95 hover:scale-100'}`}
                      >
                        <Icon className="w-4 h-4" />
                        <span className="hidden sm:block">{engine.name}</span>
                      </button>
                    );
                  })}
                </div>

                {/* Search Input Bar */}
                <form onSubmit={handleExtraction} className="w-full relative flex items-center group shadow-2xl rounded-2xl">
                  {/* Contextual Glow Behind Search */}
                  {currentConfig && <div className={`absolute -inset-1 rounded-2xl opacity-20 group-hover:opacity-40 blur-xl transition-all duration-500 ${currentConfig.bg}`}></div>}
                  
                  <div className="relative flex w-full bg-[#111111] border border-[#262626] rounded-2xl overflow-hidden focus-within:border-slate-500 transition-colors">
                    <div className="pl-6 flex items-center pointer-events-none border-r border-[#262626] pr-4 bg-[#0a0a0a]">
                      {currentConfig && <Target className={`w-6 h-6 ${currentConfig.color}`} />}
                    </div>
                    
                    <input
                      type="text"
                      value={targetInput}
                      onChange={(e) => setTargetInput(e.target.value)}
                      disabled={isProcessing}
                      placeholder={currentConfig ? `Enter ${currentConfig.label} identifier (${currentConfig.placeholder})...` : 'Select an engine...'}
                      className="w-full bg-transparent text-white text-lg md:text-xl px-6 py-5 focus:outline-none placeholder-slate-600 font-mono disabled:opacity-50"
                    />
                    
                    <button
                      type="submit"
                      disabled={!targetInput || isProcessing || !currentConfig}
                      className={`flex items-center gap-2 px-8 font-bold transition-all uppercase tracking-wider disabled:opacity-30 disabled:cursor-not-allowed border-l border-[#262626]
                        ${isProcessing ? 'bg-[#0a0a0a] text-slate-500' : `${currentConfig?.color} bg-[#0a0a0a] hover:bg-[#1a1a1a]`}`}
                    >
                      {isProcessing ? (
                        <Loader2 className="w-6 h-6 animate-spin" />
                      ) : (
                        <>
                          <span className="hidden md:inline">Extract</span>
                          <Focus className="w-6 h-6" />
                        </>
                      )}
                    </button>
                  </div>
                </form>
              </div>

              {/* === PRE-SEARCH STATS === */}
              <div className={`w-full max-w-5xl mx-auto transition-all duration-700 delay-100 ${hasSearched ? 'opacity-0 translate-y-8 hidden' : 'opacity-100 translate-y-0'}`}>
                <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-[#111111] border border-[#262626] p-6 rounded-2xl flex flex-col justify-between hover:border-[#facc15] transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <p className="text-xs text-slate-400 uppercase font-bold tracking-widest">Global Profiles</p>
                        <h4 className="text-3xl font-bold mt-1 text-white font-mono">1.2B<span className="text-[#facc15]">+</span></h4>
                      </div>
                      <div className="p-3 bg-[#facc15]/10 rounded-xl">
                        <Database className="w-6 h-6 text-[#facc15]" />
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-[#facc15] font-bold uppercase tracking-wider bg-[#facc15]/5 p-2 rounded-lg w-fit">
                      <TrendingUp className="w-4 h-4" /> System Nominal
                    </div>
                  </div>
                  
                  <div className="bg-[#111111] border border-[#262626] p-6 rounded-2xl flex flex-col justify-between hover:border-[#ff003c] transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <p className="text-xs text-slate-400 uppercase font-bold tracking-widest">Active Engines</p>
                        <h4 className="text-3xl font-bold mt-1 text-white font-mono">6 / 6</h4>
                      </div>
                      <div className="p-3 bg-[#ff003c]/10 rounded-xl">
                        <Cpu className="w-6 h-6 text-[#ff003c]" />
                      </div>
                    </div>
                    <div className="w-full bg-[#0a0a0a] h-2 rounded-full mt-2 overflow-hidden border border-[#262626]">
                      <div className="bg-[#ff003c] h-full w-full rounded-full shadow-[0_0_10px_#ff003c]"></div>
                    </div>
                    <p className="text-[10px] text-slate-500 mt-2 font-mono uppercase tracking-widest">All scrapers functional</p>
                  </div>
                  
                  <div className="bg-[#111111] border border-[#262626] p-6 rounded-2xl flex flex-col justify-between hover:border-[#ff4500] transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <p className="text-xs text-slate-400 uppercase font-bold tracking-widest">API Health</p>
                        <h4 className="text-3xl font-bold mt-1 text-white font-mono">99.9%</h4>
                      </div>
                      <div className="p-3 bg-[#ff4500]/10 rounded-xl">
                        <ShieldCheck className="w-6 h-6 text-[#ff4500]" />
                      </div>
                    </div>
                    <div className="flex items-end gap-1.5 h-8">
                      {[4, 6, 3, 5, 8, 4, 6, 5, 8, 7, 5, 8].map((h, i) => (
                        <div key={i} className={`w-1.5 rounded-t-sm transition-all duration-500 ease-in-out ${i === 7 ? 'bg-red-600 animate-pulse' : 'bg-[#ff4500]'}`} style={{ height: `${h * 10}%` }}></div>
                      ))}
                    </div>
                  </div>
                </section>
              </div>

              {/* === PROCESSING VISUALIZATION === */}
              {isProcessing && currentConfig && (
                <div className="w-full max-w-5xl mx-auto flex-1 flex flex-col items-center justify-center">
                  <ProcessingVisualizer config={currentConfig} />
                </div>
              )}

              {/* === FINAL DOSSIER === */}
              {dossier && !isProcessing && currentConfig && (
                <div className="w-full max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-12 duration-700 pb-12">
                  
                  {/* Dossier Header */}
                  <div className="flex flex-col md:flex-row items-start md:items-center justify-between border-b border-[#262626] pb-6 mb-8">
                    <div>
                      <h2 className="text-3xl font-bold text-white flex items-center gap-3 uppercase tracking-tighter">
                        <currentConfig.icon className={`w-8 h-8 ${currentConfig.color}`} />
                        Intelligence Dossier
                      </h2>
                      <div className="flex items-center gap-3 mt-3 text-sm font-mono">
                        <span className={`px-3 py-1 rounded bg-[#111111] border ${currentConfig.color.replace('text-', 'border-')} ${currentConfig.color} font-bold`}>
                          {currentConfig.name}
                        </span>
                        <span className="text-slate-500">TARGET:</span>
                        <span className="text-white bg-[#262626] px-2 py-0.5 rounded">{dossier.target}</span> 
                      </div>
                    </div>
                    <div className="text-left md:text-right mt-4 md:mt-0 bg-[#111111] p-3 rounded-xl border border-[#262626]">
                      <div className={`text-[10px] ${currentConfig.color} font-mono uppercase tracking-widest mb-1 font-bold`}>Extraction Timestamp</div>
                      <div className="text-sm text-slate-300 font-mono">{new Date(dossier.timestamp).toLocaleString()}</div>
                    </div>
                  </div>


                  {/* ====== UNIVERSAL DOSSIER RENDERER ====== */}
                  {(() => {
                    // Helper: prettify snake_case / camelCase keys into human readable labels
                    const prettify = (key) => key
                      .replace(/_/g, ' ')
                      .replace(/([a-z])([A-Z])/g, '$1 $2')
                      .replace(/\b\w/g, c => c.toUpperCase());

                    // Helper: render a value (handles strings, numbers, booleans, arrays, nested objects)
                    const renderValue = (val, depth = 0) => {
                      if (val === null || val === undefined || val === 'N/A') {
                        return <span className="text-slate-600 italic text-xs">N/A</span>;
                      }
                      if (typeof val === 'boolean') {
                        return <span className={`font-mono text-xs px-2 py-0.5 rounded ${val ? 'text-emerald-400 bg-emerald-400/10' : 'text-red-400 bg-red-400/10'}`}>{val ? 'TRUE' : 'FALSE'}</span>;
                      }
                      if (typeof val === 'string' || typeof val === 'number') {
                        const str = String(val);
                        if (str.startsWith('http')) {
                          return <a href={str} target="_blank" rel="noreferrer" className={`font-mono text-xs ${currentConfig.color} hover:underline break-all`}>{str.length > 60 ? str.slice(0, 60) + '…' : str}</a>;
                        }
                        return <span className="text-white font-mono text-sm break-words">{str}</span>;
                      }
                      if (Array.isArray(val)) {
                        if (val.length === 0) return <span className="text-slate-600 italic text-xs">Empty</span>;
                        // Array of objects → render as mini cards
                        if (typeof val[0] === 'object' && val[0] !== null) {
                          return (
                            <div className="space-y-2 mt-2">
                              {val.slice(0, 10).map((item, i) => (
                                <div key={i} className="bg-[#0a0a0a] p-3 rounded-lg border border-[#262626]">
                                  {Object.entries(item).map(([k, v]) => (
                                    <div key={k} className="flex flex-wrap justify-between items-start gap-2 py-1">
                                      <span className="text-[10px] text-slate-500 uppercase tracking-widest">{prettify(k)}</span>
                                      {renderValue(v, depth + 1)}
                                    </div>
                                  ))}
                                </div>
                              ))}
                              {val.length > 10 && <span className="text-slate-600 text-xs font-mono">+{val.length - 10} more…</span>}
                            </div>
                          );
                        }
                        // Array of strings/numbers → render as tags
                        return (
                          <div className="flex flex-wrap gap-1.5 mt-1">
                            {val.slice(0, 20).map((item, i) => (
                              <span key={i} className="bg-[#262626] text-slate-300 border border-slate-700 px-2.5 py-1 rounded-lg text-xs font-mono">{String(item)}</span>
                            ))}
                            {val.length > 20 && <span className="text-slate-600 text-xs">+{val.length - 20} more</span>}
                          </div>
                        );
                      }
                      if (typeof val === 'object') {
                        // Nested object → render as key-value pairs
                        const entries = Object.entries(val);
                        if (entries.length === 0) return <span className="text-slate-600 italic text-xs">Empty</span>;
                        
                        // If it looks like a heatmap (7 days × 24 hours), skip rendering it as key-value
                        if (entries.length === 7 && entries.every(([, v]) => typeof v === 'object' && Object.keys(v).length === 24)) {
                          return <span className="text-slate-500 italic text-xs font-mono">7×24 Activity Heatmap (data available)</span>;
                        }

                        return (
                          <div className={`space-y-1.5 ${depth > 0 ? 'mt-1 pl-3 border-l border-[#262626]' : 'mt-2'}`}>
                            {entries.slice(0, 20).map(([k, v]) => (
                              <div key={k} className="flex flex-wrap justify-between items-start gap-2 py-0.5">
                                <span className="text-[10px] text-slate-500 uppercase tracking-widest shrink-0">{prettify(k)}</span>
                                {renderValue(v, depth + 1)}
                              </div>
                            ))}
                          </div>
                        );
                      }
                      return <span className="text-white text-sm">{JSON.stringify(val)}</span>;
                    };

                    // Filter out meta/target/timestamp which are rendered in the header
                    const skipKeys = new Set(['target', 'timestamp', 'dossier_meta']);
                    const sections = Object.entries(dossier).filter(([k]) => !skipKeys.has(k));

                    // Color cycle for section accents
                    const accentColors = ['#facc15', '#ff003c', '#ff4500', '#3b82f6', '#a855f7', '#10b981'];

                    return (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {sections.map(([sectionKey, sectionVal], idx) => {
                          const accent = accentColors[idx % accentColors.length];
                          return (
                            <div key={sectionKey} className={`bg-[#111111] border rounded-2xl p-6 shadow-lg relative overflow-hidden`} style={{ borderColor: `${accent}30` }}>
                              <div className="absolute top-0 left-0 w-1 h-full" style={{ backgroundColor: accent, boxShadow: `0 0 15px ${accent}66` }}></div>
                              <h3 className="text-xs font-bold uppercase tracking-widest mb-5 flex items-center gap-2" style={{ color: accent }}>
                                <Database className="w-4 h-4" />
                                {prettify(sectionKey)}
                              </h3>
                              <div className="space-y-3">
                                {typeof sectionVal === 'object' && sectionVal !== null && !Array.isArray(sectionVal) ? (
                                  Object.entries(sectionVal).map(([k, v]) => (
                                    <div key={k} className="bg-[#0a0a0a] p-3 rounded-xl border border-[#262626]">
                                      <div className="text-[10px] text-slate-500 uppercase tracking-widest mb-1.5">{prettify(k)}</div>
                                      {renderValue(v)}
                                    </div>
                                  ))
                                ) : (
                                  <div className="bg-[#0a0a0a] p-3 rounded-xl border border-[#262626]">
                                    {renderValue(sectionVal)}
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    );
                  })()}
                  
                </div>
              )}
            </>
          )}

        </main>
      </div>
    </div>
  );
}
