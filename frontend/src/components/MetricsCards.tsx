import React from 'react';
import { Brain, ShieldAlert, CheckCircle2, Zap } from 'lucide-react';

interface MetricsCardsProps {
  totalMemories: number;
  incidentCount: number;
  recurrentCount: number;
}

export const MetricsCards: React.FC<MetricsCardsProps> = ({ totalMemories, incidentCount, recurrentCount }) => {
  const cards = [
    {
      title: 'Biomimetic Memory Bank',
      value: totalMemories.toString(),
      subtitle: 'World, Experience, Observation, Opinion',
      icon: Brain,
      color: '#38bdf8',
      bgGlow: 'rgba(56, 189, 248, 0.1)',
      borderColor: 'rgba(56, 189, 248, 0.2)'
    },
    {
      title: 'Recurrence Detection',
      value: `${recurrentCount} / ${incidentCount || 2}`,
      subtitle: 'Incidents matched to prior post-mortems',
      icon: ShieldAlert,
      color: '#c084fc',
      bgGlow: 'rgba(192, 132, 252, 0.1)',
      borderColor: 'rgba(192, 132, 252, 0.2)'
    },
    {
      title: 'Continuous Compliance',
      value: '100%',
      subtitle: 'SOC 2 CC6.1 & NIST PR.AC-04 readiness',
      icon: CheckCircle2,
      color: '#34d399',
      bgGlow: 'rgba(52, 211, 153, 0.1)',
      borderColor: 'rgba(52, 211, 153, 0.2)'
    },
    {
      title: 'Avg Triage & Hash Speed',
      value: '< 2.5s',
      subtitle: 'Automated RCA & SHA-256 evidence proof',
      icon: Zap,
      color: '#fbbf24',
      bgGlow: 'rgba(251, 191, 36, 0.1)',
      borderColor: 'rgba(251, 191, 36, 0.2)'
    }
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
      {cards.map((c, idx) => {
        const Icon = c.icon;
        return (
          <div
            key={idx}
            className="glass-panel"
            style={{
              padding: '1.25rem',
              position: 'relative',
              overflow: 'hidden',
              borderColor: c.borderColor
            }}
          >
            {/* Background subtle glow */}
            <div style={{
              position: 'absolute',
              top: '-20px',
              right: '-20px',
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              background: c.bgGlow,
              filter: 'blur(30px)',
              pointerEvents: 'none'
            }} />

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 500 }}>
                {c.title}
              </span>
              <div style={{
                background: c.bgGlow,
                border: `1px solid ${c.borderColor}`,
                padding: '0.4rem',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Icon size={18} color={c.color} />
              </div>
            </div>

            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fff', letterSpacing: '-0.03em', lineHeight: 1.1 }}>
              {c.value}
            </div>

            <p style={{ color: 'var(--text-dim)', fontSize: '0.75rem', marginTop: '0.4rem' }}>
              {c.subtitle}
            </p>
          </div>
        );
      })}
    </div>
  );
};
