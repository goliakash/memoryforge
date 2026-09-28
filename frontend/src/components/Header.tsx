import React from 'react';
import { Brain, ShieldCheck, Activity, Terminal, Database, FileCheck, Layers } from 'lucide-react';
import type { SystemHealth } from '../types/api';

interface HeaderProps {
  health: SystemHealth | null;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRefreshHealth: () => void;
  onResetMemory: () => void;
}

export const Header: React.FC<HeaderProps> = ({ health, activeTab, setActiveTab, onRefreshHealth, onResetMemory }) => {
  const isHealthy = health?.status === 'healthy';
  const totalMemories = health?.networks_status?.total_memories || 0;
  const networks = health?.networks_status?.networks || { world: 0, experience: 0, observation: 0, opinion: 0 };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'investigate', label: 'AI Incident Triage', icon: ShieldCheck },
    { id: 'memories', label: 'Memory Bank Explorer', icon: Database },
    { id: 'audit', label: 'Auditor Portal', icon: FileCheck },
    { id: 'demo', label: '10-Step Automated Story', icon: Terminal },
  ];

  return (
    <header className="glass-panel" style={{ borderRadius: '0 0 16px 16px', marginBottom: '2rem', padding: '1rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        
        {/* Brand & Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{
            background: 'linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)',
            padding: '0.65rem',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(14, 165, 233, 0.4)'
          }}>
            <Brain size={26} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <h1 className="gradient-text" style={{ fontSize: '1.4rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
                Memory Forge
              </h1>
              <span className="badge badge-violet" style={{ fontSize: '0.65rem' }}>v1.0</span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '-2px' }}>
              Persistent Organizational Memory for SecOps & Compliance
            </p>
          </div>
        </div>

        {/* Live Biomimetic Memory Pointers & Health */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          
          {/* Biomimetic Memory Networks Counter */}
          <div style={{
            background: 'rgba(15, 23, 42, 0.6)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            padding: '0.4rem 0.85rem',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            fontSize: '0.8rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Layers size={14} color="#38bdf8" />
              <span style={{ color: 'var(--text-muted)' }}>Memories:</span>
              <strong style={{ color: '#38bdf8' }}>{totalMemories}</strong>
            </div>
            <div style={{ width: '1px', height: '14px', background: 'rgba(255,255,255,0.1)' }} />
            <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.75rem' }}>
              <span title="World Network (Baselines)"><strong style={{ color: '#60a5fa' }}>W:</strong>{networks.world}</span>
              <span title="Experience Network (Incidents)"><strong style={{ color: '#c084fc' }}>E:</strong>{networks.experience}</span>
              <span title="Observation Network (Patterns)"><strong style={{ color: '#34d399' }}>O:</strong>{networks.observation}</span>
              <span title="Opinion Network (Beliefs)"><strong style={{ color: '#fbbf24' }}>Op:</strong>{networks.opinion}</span>
            </div>
          </div>

          {/* Reset Memory Bank Button */}
          <button
            onClick={onResetMemory}
            title="Reset memory bank to 0 memories"
            style={{
              background: 'rgba(244, 63, 94, 0.1)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              color: '#fb7185',
              padding: '0.4rem 0.65rem',
              borderRadius: '10px',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}
          >
            Reset (0)
          </button>

          {/* Backend Status Indicator */}
          <button 
            onClick={onRefreshHealth} 
            title="Click to re-check FastAPI connection"
            style={{
              background: 'rgba(15, 23, 42, 0.6)',
              border: `1px solid ${isHealthy ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`,
              padding: '0.4rem 0.75rem',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              fontSize: '0.8rem',
              color: isHealthy ? '#34d399' : '#fb7185'
            }}
          >
            <div className={isHealthy ? 'pulse-dot' : ''} style={{ background: isHealthy ? '#10b981' : '#f43f5e' }} />
            <span>{isHealthy ? 'API Online :8000' : 'Offline Mode'}</span>
          </button>

        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', gap: '0.5rem', marginTop: '1.25rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '0.85rem' }}>
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                background: isActive ? 'linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%)' : 'transparent',
                border: isActive ? '1px solid rgba(14, 165, 233, 0.4)' : '1px solid transparent',
                color: isActive ? '#38bdf8' : 'var(--text-muted)',
                padding: '0.5rem 1rem',
                borderRadius: '8px',
                fontWeight: isActive ? 600 : 400,
                fontSize: '0.85rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.45rem',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={16} color={isActive ? '#38bdf8' : '#94a3b8'} />
              {tab.label}
            </button>
          );
        })}
      </nav>
    </header>
  );
};
