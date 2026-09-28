import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { MetricsCards } from './components/MetricsCards';
import { BiomimeticNetworks } from './components/BiomimeticNetworks';
import { IncidentInvestigator } from './components/IncidentInvestigator';
import { IncidentHistoryTable } from './components/IncidentHistoryTable';
import { MemoryExplorer } from './components/MemoryExplorer';
import { AuditorPortal } from './components/AuditorPortal';
import { DemoStoryRunner } from './components/DemoStoryRunner';
import type { SystemHealth, IncidentRecord } from './types/api';
import { apiService } from './services/api';
import { X, AlertTriangle, Hash } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<IncidentRecord | null>(null);
  const [selectedNetwork, setSelectedNetwork] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth();
    fetchIncidents();
  }, []);

  const fetchHealth = async () => {
    try {
      const data = await apiService.getHealth();
      setHealth(data);
    } catch (err) {
      console.error('Failed to load health:', err);
    }
  };

  const fetchIncidents = async () => {
    try {
      const data = await apiService.getIncidents();
      setIncidents(data);
    } catch (err) {
      console.error('Failed to load incidents:', err);
    }
  };

  const handleResetMemory = async () => {
    try {
      const data = await apiService.clearMemory();
      setHealth(data);
      setIncidents([]);
    } catch (err) {
      console.error('Failed to reset memory:', err);
    }
  };

  const handleIncidentInvestigated = (newRecord: IncidentRecord) => {
    setIncidents(prev => [newRecord, ...prev]);
    fetchHealth(); // refresh memory count
  };

  const handleExploreNetwork = (networkId: string) => {
    setSelectedNetwork(networkId);
    setActiveTab('memories');
  };

  const recurrentCount = incidents.filter(i => i.is_recurring).length;
  const totalMemories = health?.networks_status?.total_memories || 0;
  const networksCounts = health?.networks_status?.networks || { world: 0, experience: 0, observation: 0, opinion: 0 };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 1.5rem 3rem' }}>
      
      {/* Header Bar */}
      <Header
        health={health}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefreshHealth={fetchHealth}
        onResetMemory={handleResetMemory}
      />

      {/* Overview Dashboard Tab */}
      {activeTab === 'overview' && (
        <>
          <MetricsCards
            totalMemories={totalMemories}
            incidentCount={incidents.length}
            recurrentCount={recurrentCount}
          />

          <BiomimeticNetworks
            counts={networksCounts}
            onExploreNetwork={handleExploreNetwork}
          />

          <IncidentInvestigator
            onIncidentInvestigated={handleIncidentInvestigated}
          />

          <IncidentHistoryTable
            incidents={incidents}
            onSelectIncident={setSelectedIncident}
          />
        </>
      )}

      {/* AI Triage Tab */}
      {activeTab === 'investigate' && (
        <>
          <IncidentInvestigator
            onIncidentInvestigated={handleIncidentInvestigated}
          />
          <IncidentHistoryTable
            incidents={incidents}
            onSelectIncident={setSelectedIncident}
          />
        </>
      )}

      {/* Memory Explorer Tab */}
      {activeTab === 'memories' && (
        <MemoryExplorer initialNetwork={selectedNetwork} />
      )}

      {/* Auditor Portal Tab */}
      {activeTab === 'audit' && (
        <AuditorPortal />
      )}

      {/* 10-Step Automated Story Tab */}
      {activeTab === 'demo' && (
        <DemoStoryRunner />
      )}

      {/* Incident Detail Modal */}
      {selectedIncident && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(8, 12, 20, 0.85)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '1.5rem'
        }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '750px', maxHeight: '90vh', overflowY: 'auto', padding: '2rem', position: 'relative' }}>
            
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>
              <div>
                <span className="badge badge-cyan" style={{ fontFamily: 'var(--font-mono)', marginBottom: '0.25rem' }}>
                  {selectedIncident.incident_id}
                </span>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff' }}>
                  {selectedIncident.title}
                </h3>
              </div>
              
              <button
                onClick={() => setSelectedIncident(null)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={24} />
              </button>
            </div>

            {/* Recurrence banner */}
            {selectedIncident.is_recurring && (
              <div style={{ background: 'rgba(139, 92, 246, 0.2)', border: '1px solid rgba(192, 132, 252, 0.4)', padding: '0.85rem 1rem', borderRadius: '10px', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <AlertTriangle size={20} color="#c084fc" />
                <span style={{ color: '#e9d5ff', fontSize: '0.85rem' }}>
                  Recurrent Incident: Matched <strong>{selectedIncident.recalled_incident_id}</strong> with <strong>{Math.round((selectedIncident.similarity_score || 0.9) * 100)}% similarity</strong>.
                </span>
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>System & Severity</h4>
                <div style={{ color: '#fff', fontSize: '0.9rem' }}>
                  {selectedIncident.affected_system} • <span className="badge badge-rose">{selectedIncident.severity}</span>
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Root Cause Analysis</h4>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', padding: '0.85rem 1rem', borderRadius: '8px', fontSize: '0.85rem', color: '#e2e8f0' }}>
                  {selectedIncident.root_cause}
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Mapped Controls</h4>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {selectedIncident.mapped_controls?.map((ctrl, i) => (
                    <span key={i} className="badge badge-emerald">
                      {ctrl.framework} {ctrl.control_id}: {ctrl.name}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Cryptographic Evidence</h4>
                {selectedIncident.evidence_fingerprints?.map((ev, i) => (
                  <div key={i} className="code-box" style={{ fontSize: '0.75rem', marginBottom: '0.35rem' }}>
                    <Hash size={12} color="#38bdf8" /> {ev.sha256_hash}
                  </div>
                ))}
              </div>

              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Remediation Steps</h4>
                <ul style={{ paddingLeft: '1.2rem', color: '#cbd5e1', fontSize: '0.825rem' }}>
                  {selectedIncident.remediation_playbook?.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={{ marginTop: '3rem', textTransform: 'uppercase', letterSpacing: '0.05em', textAlign: 'center', color: 'var(--text-dim)', fontSize: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '1.5rem' }}>
        AI Security Operations & Compliance Memory Agent • Powered by Hindsight • FastAPI & React
      </footer>

    </div>
  );
}

export default App;
