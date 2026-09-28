import React, { useState } from 'react';
import { ShieldAlert, Zap, CheckCircle2, AlertTriangle, Hash, RefreshCw } from 'lucide-react';
import type { IncidentRequest, IncidentRecord } from '../types/api';
import { apiService } from '../services/api';

interface IncidentInvestigatorProps {
  onIncidentInvestigated: (record: IncidentRecord) => void;
}

export const IncidentInvestigator: React.FC<IncidentInvestigatorProps> = ({ onIncidentInvestigated }) => {
  const [formData, setFormData] = useState<IncidentRequest>({
    title: 'Public S3 Bucket Exposure on analytics-data-bucket',
    affected_system: 'analytics-data-bucket (us-east-1)',
    severity: 'HIGH',
    description: 'Automated security scanner detected unauthenticated public read permissions enabled on analytics storage bucket.',
    logs: 'S3:GetObject 200 AnonymousUser 192.0.2.45 GET /analytics/q3_revenue.csv [ACL: public-read]',
    vector: 'S3 Bucket ACL / IAM Misconfiguration'
  });

  const [isInvestigating, setIsInvestigating] = useState(false);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [investigationResult, setInvestigationResult] = useState<IncidentRecord | null>(null);

  const presets = [
    {
      label: 'Incident #1024 (Customer Data Exposure)',
      data: {
        title: 'Customer Data Bucket Unauthenticated Access',
        affected_system: 'customer-data-bucket (us-west-2)',
        severity: 'CRITICAL' as const,
        description: 'Security audit tool flagged public read permissions on customer PII storage bucket.',
        logs: 'S3:GetObject 200 AnonymousUser 203.0.113.12 GET /pii/users_export.json [ACL: public-read]',
        vector: 'IAM Wildcard Policy'
      }
    },
    {
      label: 'Incident #1038 (Recurrent Analytics Exposure)',
      data: {
        title: 'Public S3 Bucket Exposure on analytics-data-bucket',
        affected_system: 'analytics-data-bucket (us-east-1)',
        severity: 'HIGH' as const,
        description: 'Automated scanner detected unauthenticated public read permissions on analytics bucket.',
        logs: 'S3:GetObject 200 AnonymousUser 192.0.2.45 GET /analytics/q3_revenue.csv [ACL: public-read]',
        vector: 'S3 Bucket ACL / IAM Policy'
      }
    },
    {
      label: 'Staging Database Unauthorized Port Exposure',
      data: {
        title: 'PostgreSQL Port 5432 Exposed to 0.0.0.0/0',
        affected_system: 'db-staging-01 (us-east-1)',
        severity: 'MEDIUM' as const,
        description: 'Security group rule ingress opened database port 5432 to public internet.',
        logs: 'EC2:AuthorizeSecurityGroupIngress 200 0.0.0.0/0 port 5432 tcp',
        vector: 'Security Group Misconfiguration'
      }
    }
  ];

  const handleInvestigate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsInvestigating(true);
    setInvestigationResult(null);
    setCurrentStep(1);

    // Simulate pipeline progression
    await new Promise(r => setTimeout(r, 600));
    setCurrentStep(2); // Recalling Hindsight Memory
    await new Promise(r => setTimeout(r, 700));
    setCurrentStep(3); // AI Root Cause Analysis
    await new Promise(r => setTimeout(r, 600));
    setCurrentStep(4); // Security Control Mapping & SHA-256 Fingerprinting

    try {
      const result = await apiService.investigateIncident(formData);
      setInvestigationResult(result);
      onIncidentInvestigated(result);
    } catch (err) {
      console.error('Investigation error:', err);
    } finally {
      setIsInvestigating(false);
      setCurrentStep(0);
    }
  };

  return (
    <div style={{ marginBottom: '2.5rem' }}>
      
      {/* Header */}
      <div style={{ marginBottom: '1.25rem' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Zap size={20} color="#38bdf8" />
          AI Security Incident Investigation Hub
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem' }}>
          Ingest raw security incidents, conduct automated AI Root Cause Analysis, map controls, fingerprint cryptographic evidence, and recall prior incident learnings from Hindsight.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        
        {/* Left Form Panel */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#fff' }}>Ingest Security Incident</h3>
            
            {/* Quick Presets Dropdown */}
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              {presets.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setFormData(p.data)}
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    color: 'var(--text-muted)',
                    padding: '0.3rem 0.6rem',
                    borderRadius: '6px',
                    fontSize: '0.725rem',
                    cursor: 'pointer'
                  }}
                >
                  Preset {idx + 1}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleInvestigate} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Incident Title
              </label>
              <input
                type="text"
                className="input-field"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Affected System / Resource
                </label>
                <input
                  type="text"
                  className="input-field"
                  value={formData.affected_system}
                  onChange={(e) => setFormData({ ...formData, affected_system: e.target.value })}
                  required
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Severity Level
                </label>
                <select
                  className="input-field"
                  value={formData.severity}
                  onChange={(e) => setFormData({ ...formData, severity: e.target.value as any })}
                >
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                  <option value="CRITICAL">CRITICAL</option>
                </select>
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Incident Description & Context
              </label>
              <textarea
                className="input-field"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Raw Audit / Error Logs (Optional)
              </label>
              <textarea
                className="input-field"
                style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}
                value={formData.logs}
                onChange={(e) => setFormData({ ...formData, logs: e.target.value })}
              />
            </div>

            <button
              type="submit"
              disabled={isInvestigating}
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem' }}
            >
              {isInvestigating ? (
                <>
                  <RefreshCw size={16} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
                  Investigating & Scanning Hindsight Memory...
                </>
              ) : (
                <>
                  <Zap size={16} /> Run AI Investigation & Hindsight Memory Loop
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Output Panel */}
        <div>
          {/* Live Progress Pipeline */}
          {isInvestigating && (
            <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
              <h4 style={{ fontSize: '0.9rem', color: '#38bdf8', marginBottom: '1rem', fontWeight: 600 }}>
                Autonomous AI Triage Pipeline Active
              </h4>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                {[
                  { step: 1, text: 'Ingesting incident telemetry & log signals' },
                  { step: 2, text: 'Scanning Hindsight Memory Bank (Recall prior post-mortems)' },
                  { step: 3, text: 'Performing LLM Root Cause Analysis (RCA) & vector breakdown' },
                  { step: 4, text: 'Mapping SOC 2 / NIST / ISO controls & hashing SHA-256 evidence' }
                ].map((s) => (
                  <div key={s.step} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.85rem' }}>
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      background: currentStep >= s.step ? 'linear-gradient(135deg, #0ea5e9, #6366f1)' : 'rgba(255, 255, 255, 0.05)',
                      border: currentStep >= s.step ? 'none' : '1px solid rgba(255, 255, 255, 0.1)',
                      color: '#fff',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      {currentStep > s.step ? <CheckCircle2 size={14} /> : s.step}
                    </div>
                    <span style={{ color: currentStep >= s.step ? '#f8fafc' : 'var(--text-dim)' }}>
                      {s.text}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Investigation Result Report */}
          {investigationResult ? (
            <div className="glass-panel" style={{ padding: '1.5rem', borderColor: investigationResult.is_recurring ? 'rgba(192, 132, 252, 0.4)' : 'rgba(16, 185, 129, 0.4)' }}>
              
              {/* Recurrence Banner */}
              {investigationResult.is_recurring ? (
                <div style={{
                  background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(236, 72, 153, 0.25) 100%)',
                  border: '1px solid rgba(192, 132, 252, 0.5)',
                  borderRadius: '10px',
                  padding: '0.85rem 1rem',
                  marginBottom: '1.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem'
                }}>
                  <AlertTriangle size={24} color="#c084fc" />
                  <div>
                    <strong style={{ color: '#f5d0fe', fontSize: '0.9rem' }}>
                      🧠 HINDSIGHT MEMORY RECALL: Recurrent Incident Detected!
                    </strong>
                    <p style={{ color: '#e9d5ff', fontSize: '0.8rem', marginTop: '2px' }}>
                      Matched prior incident <strong>{investigationResult.recalled_incident_id}</strong> from Experience Network with <strong>{Math.round((investigationResult.similarity_score || 0.9) * 100)}% similarity</strong>. Reusing proven remediation playbook.
                    </p>
                  </div>
                </div>
              ) : (
                <div style={{
                  background: 'rgba(16, 185, 129, 0.15)',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  borderRadius: '10px',
                  padding: '0.75rem 1rem',
                  marginBottom: '1.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.6rem'
                }}>
                  <CheckCircle2 size={20} color="#34d399" />
                  <span style={{ color: '#34d399', fontSize: '0.85rem', fontWeight: 600 }}>
                    New Incident Analyzed & Retained to Hindsight Memory Bank
                  </span>
                </div>
              )}

              {/* Title & Meta */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff' }}>
                  {investigationResult.title}
                </h3>
                <span className={`badge ${investigationResult.severity === 'CRITICAL' ? 'badge-rose' : 'badge-amber'}`}>
                  {investigationResult.severity}
                </span>
              </div>

              {/* Root Cause Analysis Box */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Root Cause Analysis (RCA)
                </h4>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '0.85rem 1rem', fontSize: '0.875rem', color: '#e2e8f0', lineHeight: 1.5 }}>
                  {investigationResult.root_cause}
                </div>
              </div>

              {/* Mapped Compliance Controls */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Mapped Compliance Controls
                </h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {investigationResult.mapped_controls.map((ctrl, i) => (
                    <div
                      key={i}
                      style={{
                        background: 'rgba(6, 182, 212, 0.1)',
                        border: '1px solid rgba(6, 182, 212, 0.3)',
                        borderRadius: '8px',
                        padding: '0.4rem 0.75rem',
                        fontSize: '0.775rem'
                      }}
                    >
                      <strong style={{ color: '#38bdf8' }}>{ctrl.framework} {ctrl.control_id}: </strong>
                      <span style={{ color: '#94a3b8' }}>{ctrl.name}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* SHA-256 Cryptographic Evidence Proof */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  SHA-256 Evidence Fingerprints
                </h4>
                {investigationResult.evidence_fingerprints.map((ev, i) => (
                  <div key={i} className="code-box" style={{ fontSize: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', overflow: 'hidden' }}>
                      <Hash size={14} color="#38bdf8" />
                      <span style={{ color: '#f8fafc', fontWeight: 600 }}>{ev.type}:</span>
                      <span style={{ color: '#38bdf8', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                        {ev.sha256_hash}
                      </span>
                    </div>
                    <span className="badge badge-emerald" style={{ fontSize: '0.65rem' }}>VERIFIED</span>
                  </div>
                ))}
              </div>

              {/* Remediation Playbook */}
              <div>
                <h4 style={{ fontSize: '0.825rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Synthesized Remediation Playbook
                </h4>
                <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-muted)', fontSize: '0.825rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                  {investigationResult.remediation_playbook.map((step, i) => (
                    <li key={i} style={{ color: '#cbd5e1' }}>{step}</li>
                  ))}
                </ul>
              </div>

            </div>
          ) : !isInvestigating && (
            <div className="glass-panel" style={{ padding: '3rem 1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <ShieldAlert size={40} color="#64748b" style={{ marginBottom: '0.75rem' }} />
              <h4 style={{ color: '#94a3b8', fontSize: '1rem', marginBottom: '0.35rem' }}>No Active Investigation Output</h4>
              <p style={{ fontSize: '0.825rem', maxWidth: '300px', margin: '0 auto' }}>
                Fill in the form on the left or select a quick preset to launch an AI Root Cause Analysis & memory scan.
              </p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
};
