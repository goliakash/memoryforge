import React from 'react';
import { Globe, History, Eye, Lightbulb, ChevronRight, Sparkles } from 'lucide-react';
import type { MemoryNetworkCounts } from '../types/api';

interface BiomimeticNetworksProps {
  counts: MemoryNetworkCounts;
  onExploreNetwork: (network: string) => void;
}

export const BiomimeticNetworks: React.FC<BiomimeticNetworksProps> = ({ counts, onExploreNetwork }) => {

  const networks = [
    {
      id: 'world',
      title: 'World Network',
      cognitiveRole: 'Objective Standards & Policies',
      count: counts.world,
      description: 'Encodes compliance frameworks (SOC 2, NIST CSF, ISO 27001), corporate policies, baseline configurations, and zero-trust guidelines.',
      example: 'SOC 2 CC6.1 Logical Access Control requirement & AWS S3 private policy specification',
      icon: Globe,
      color: '#60a5fa',
      badgeClass: 'badge-cyan',
      borderColor: 'rgba(96, 165, 250, 0.3)'
    },
    {
      id: 'experience',
      title: 'Experience Network',
      cognitiveRole: 'Episodic Incident History & RCA',
      count: counts.experience,
      description: 'Stores detailed post-mortems, root cause analyses, investigator notes, affected systems, and exact remediation playbooks from past incidents.',
      example: 'Incident #1024 customer-data-bucket exposure & root cause IAM policy fix',
      icon: History,
      color: '#c084fc',
      badgeClass: 'badge-violet',
      borderColor: 'rgba(192, 132, 252, 0.3)'
    },
    {
      id: 'observation',
      title: 'Observation Network',
      cognitiveRole: 'Synthesized Pattern & Recurrence Detection',
      count: counts.observation,
      description: 'Distills multi-incident patterns, identifying recurring vulnerability vectors, cloud configuration drift, and system-wide security trends.',
      example: 'Observation: 2 S3 bucket exposure incidents detected within 7 days across distinct teams',
      icon: Eye,
      color: '#34d399',
      badgeClass: 'badge-emerald',
      borderColor: 'rgba(52, 211, 153, 0.3)'
    },
    {
      id: 'opinion',
      title: 'Opinion Network',
      cognitiveRole: 'Evolving Beliefs & Risk Posture',
      count: counts.opinion,
      description: 'Formulates organizational risk beliefs and preventive recommendations based on synthesized evidence and recurring incident frequency.',
      example: 'Belief: Manual IAM policy assignments carry high error rate; enforce automated guardrails in CI/CD',
      icon: Lightbulb,
      color: '#fbbf24',
      badgeClass: 'badge-amber',
      borderColor: 'rgba(251, 191, 36, 0.3)'
    }
  ];

  return (
    <div style={{ marginBottom: '2.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={20} color="#38bdf8" />
            Hindsight Biomimetic Memory Networks
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem' }}>
            The 4 cognitive memory layers powering intelligent security investigation and continuous audit readiness
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
        {networks.map((net) => {
          const Icon = net.icon;
          return (
            <div
              key={net.id}
              className="glass-panel glass-card-interactive"
              onClick={() => onExploreNetwork(net.id)}
              style={{
                padding: '1.25rem',
                borderColor: net.borderColor,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <div style={{
                      background: `rgba(${net.id === 'world' ? '96, 165, 250' : net.id === 'experience' ? '192, 132, 252' : net.id === 'observation' ? '52, 211, 153' : '251, 191, 36'}, 0.15)`,
                      padding: '0.5rem',
                      borderRadius: '10px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Icon size={20} color={net.color} />
                    </div>
                    <div>
                      <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff' }}>{net.title}</h3>
                      <span style={{ fontSize: '0.7rem', color: net.color, fontWeight: 600 }}>{net.cognitiveRole}</span>
                    </div>
                  </div>

                  <span className={`badge ${net.badgeClass}`}>
                    {net.count} units
                  </span>
                </div>

                <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', marginBottom: '0.85rem', lineHeight: 1.4 }}>
                  {net.description}
                </p>

                <div style={{
                  background: 'rgba(15, 23, 42, 0.7)',
                  border: '1px dashed rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  padding: '0.6rem 0.75rem',
                  fontSize: '0.75rem',
                  color: 'var(--text-dim)',
                  marginBottom: '1rem'
                }}>
                  <strong style={{ color: 'var(--text-muted)' }}>Example: </strong>
                  {net.example}
                </div>
              </div>

              <button
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: net.color,
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.3rem',
                  cursor: 'pointer',
                  padding: 0
                }}
              >
                Inspect Network Memories <ChevronRight size={14} />
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
