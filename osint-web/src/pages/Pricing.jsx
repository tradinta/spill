import { Check, Zap, Server, Shield } from 'lucide-react';

export default function Pricing() {
  const tiers = [
    {
      name: "Hobbyist Recon",
      price: "$0",
      icon: <Zap size={24} color="var(--accent-blue)" />,
      desc: "For basic intelligence gathering.",
      features: ["5 Manual searches/day", "Basic profile metadata", "Standard rate processing", "No API access"],
      color: "blue",
      btnText: "Start Free",
      popular: false
    },
    {
      name: "Professional Intel",
      price: "$49",
      icon: <Shield size={24} color="var(--accent-purple)" />,
      desc: "Deep behavioral analysis & tracking.",
      features: ["1,000 Searches/month", "Full behavioral heatmaps", "Interaction networks", "Priority processing", "PDF Report Generation"],
      color: "purple",
      btnText: "Upgrade to Pro",
      popular: true
    },
    {
      name: "Enterprise Node",
      price: "$299",
      icon: <Server size={24} color="var(--accent-red)" />,
      desc: "Unlimited API access for scaling.",
      features: ["Unlimited Searches", "Full REST API Access", "Stealth evasion routing", "Custom webhooks", "Dedicated account manager"],
      color: "red",
      btnText: "Contact Sales",
      popular: false
    }
  ];

  return (
    <div className="container" style={{ padding: '4rem 0' }}>
      <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h1 className="animate-fade-in" style={{ fontSize: '3rem', marginBottom: '1rem' }}>Access <span className="text-gradient">Tiers</span></h1>
        <p className="animate-fade-in stagger-1" style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
          From manual lookups to enterprise-scale automated reconnaissance.
        </p>
      </div>

      <div className="grid grid-cols-3">
        {tiers.map((t, i) => (
          <div key={t.name} className={`glass-panel animate-fade-in stagger-${i+1}`} style={{ position: 'relative', padding: '2rem', display: 'flex', flexDirection: 'column' }}>
            {t.popular && (
              <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translate(-50%, -50%)' }}>
                <span className="badge badge-purple" style={{ background: 'var(--accent-purple)', color: 'white' }}>Most Popular</span>
              </div>
            )}
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
              <div className={`badge badge-${t.color}`} style={{ padding: '0.75rem', borderRadius: '12px' }}>
                {t.icon}
              </div>
              <h2 style={{ fontSize: '1.5rem', margin: 0 }}>{t.name}</h2>
            </div>
            
            <div style={{ marginBottom: '1rem' }}>
              <span style={{ fontSize: '3rem', fontWeight: 800 }}>{t.price}</span>
              <span style={{ color: 'var(--text-secondary)' }}>/mo</span>
            </div>
            
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', flex: 1 }}>{t.desc}</p>
            
            <ul style={{ listStyle: 'none', padding: 0, marginBottom: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {t.features.map(f => (
                <li key={f} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <Check size={16} color={`var(--accent-${t.color})`} />
                  <span>{f}</span>
                </li>
              ))}
            </ul>
            
            <button className={t.popular ? 'btn-primary' : 'btn-secondary'} style={{ width: '100%' }}>
              {t.btnText}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
