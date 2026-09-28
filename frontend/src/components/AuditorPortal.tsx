import React, { useState } from 'react';
import { FileCheck, CheckCircle2, Copy } from 'lucide-react';
import type { AuditQueryResult } from '../types/api';
import { apiService } from '../services/api';

export const AuditorPortal: React.FC = () => {
  const [question, setQuestion] = useState('Show all historical S3 bucket exposure findings and cryptographic SHA-256 evidence for SOC 2 CC6.1 compliance over the past 90 days.');
  const [category, setCategory] = useState('Access Control & Infrastructure');
  const [isQuerying, setIsQuerying] = useState(false);
  const [auditResult, setAuditResult] = useState<AuditQueryResult | null>(null);
  const [copied, setCopied] = useState(false);

  const sampleQueries = [
    {
      label: 'SOC 2 CC6.1 Access Control Findings',
      category: 'Logical Access Controls',
      question: 'Provide all investigated incidents, root cause analyses, and evidence hashes mapped to SOC 2 CC6.1 Logical Access Controls.'
    },
    {
      label: 'NIST PR.AC-04 Access Permissions Audit',
      category: 'Least Privilege Management',
      question: 'Verify whether all unauthenticated data storage exposures were remediated in compliance with NIST PR.AC-04.'
    },
    {
      label: 'ISO 27001 A.5.15 Continuous Compliance Package',
      category: 'Information Security Policy',
      question: 'Synthesize full compliance report for ISO 27001 A.5.15 access control policy verification.'
    }
  ];

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsQuerying(true);
    setAuditResult(null);

    try {
      const res = await apiService.submitAuditQuery({ category, question });
      setAuditResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsQuerying(false);
    }
  };

  const copyReport = () => {
    if (!auditResult) return;
    const text = `
=== HINDSIGHT CONTINUOUS AUDIT REPORT ===
Query ID: ${auditResult.query_id}
Category: ${auditResult.category}
Compliance Status: ${auditResult.compliance_status}
Question: ${auditResult.question}

FINDINGS:
${auditResult.audit_findings.map(f => `- ${f}`).join('\n')}

VERIFIED CRYPTOGRAPHIC EVIDENCE (SHA-256):
${auditResult.evidence_hashes.map(h => `- ${h}`).join('\n')}

GUIDANCE & NEXT STEPS:
${auditResult.guidance}
Timestamp: ${auditResult.timestamp}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ marginBottom: '2.5rem' }}>
      
      {/* Header */}
      <div style={{ marginBottom: '1.25rem' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FileCheck size={20} color="#34d399" />
          Continuous Compliance & Auditor Query Portal
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem' }}>
          Query Hindsight organizational memory to instantly generate verified audit reports backed by cryptographic SHA-256 evidence.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        
        {/* Left Query Workbench */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#fff', marginBottom: '1rem' }}>
            Submit Auditor Inquiry
          </h3>

          {/* Sample Prompts */}
          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
              Sample Regulatory Templates
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
              {sampleQueries.map((sq, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setQuestion(sq.question);
                    setCategory(sq.category);
                  }}
                  style={{
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '8px',
                    padding: '0.6rem 0.85rem',
                    textAlign: 'left',
                    color: '#e2e8f0',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                  }}
                >
                  <span>{sq.label}</span>
                  <span style={{ color: '#38bdf8', fontSize: '0.7rem' }}>Use →</span>
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleQuery} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Audit Category
              </label>
              <input
                type="text"
                className="input-field"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Auditor Inquiry / Question
              </label>
              <textarea
                className="input-field"
                style={{ minHeight: '120px' }}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                required
              />
            </div>

            <button type="submit" disabled={isQuerying} className="btn-primary" style={{ justifyContent: 'center' }}>
              {isQuerying ? 'Querying Hindsight Memory Bank...' : 'Synthesize Audit Evidence Package'}
            </button>
          </form>
        </div>

        {/* Right Audit Report Package */}
        <div>
          {auditResult ? (
            <div className="glass-panel" style={{ padding: '1.5rem', borderColor: 'rgba(52, 211, 153, 0.4)' }}>
              
              {/* Top Banner */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', paddingBottom: '1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
                <div>
                  <span className="badge badge-emerald" style={{ marginBottom: '0.4rem' }}>
                    <CheckCircle2 size={12} /> {auditResult.compliance_status}
                  </span>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff' }}>
                    Continuous Audit Report #{auditResult.query_id}
                  </h3>
                </div>

                <button onClick={copyReport} className="btn-secondary" style={{ padding: '0.4rem 0.75rem', fontSize: '0.775rem' }}>
                  <Copy size={14} /> {copied ? 'Copied Report!' : 'Copy Package'}
                </button>
              </div>

              {/* Inquiry Question */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  Auditor Question
                </h4>
                <p style={{ color: '#94a3b8', fontSize: '0.85rem', fontStyle: 'italic' }}>
                  "{auditResult.question}"
                </p>
              </div>

              {/* Audit Findings List */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  Hindsight Verified Audit Findings
                </h4>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '0.85rem 1rem' }}>
                  <ul style={{ paddingLeft: '1.2rem', color: '#e2e8f0', fontSize: '0.825rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                    {auditResult.audit_findings.map((f, i) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Cryptographic SHA-256 Proofs */}
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  SHA-256 Cryptographic Verification Hashes
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {auditResult.evidence_hashes.map((hash, i) => (
                    <div key={i} className="code-box" style={{ fontSize: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span style={{ color: '#38bdf8' }}>{hash}</span>
                      <span style={{ color: '#34d399', fontSize: '0.65rem' }}>MATCHED IN MEMORY</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendation / Guidance */}
              <div>
                <h4 style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  Compliance Guidance
                </h4>
                <p style={{ color: '#cbd5e1', fontSize: '0.825rem', background: 'rgba(6, 182, 212, 0.08)', border: '1px solid rgba(6, 182, 212, 0.2)', padding: '0.65rem 0.85rem', borderRadius: '8px' }}>
                  {auditResult.guidance}
                </p>
              </div>

            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '3rem 1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <FileCheck size={40} color="#64748b" style={{ marginBottom: '0.75rem' }} />
              <h4 style={{ color: '#94a3b8', fontSize: '1rem', marginBottom: '0.35rem' }}>Auditor Package Ready</h4>
              <p style={{ fontSize: '0.825rem', maxWidth: '300px', margin: '0 auto' }}>
                Select a regulatory query template or submit your own question to generate a cryptographically verified compliance report.
              </p>
            </div>
          )}
        </div>

      </div>

    </div>
  );
};
