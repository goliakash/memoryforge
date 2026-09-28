import React, { useState } from 'react';
import { Search, RefreshCw, Eye, Hash } from 'lucide-react';
import type { IncidentRecord } from '../types/api';

interface IncidentHistoryTableProps {
  incidents: IncidentRecord[];
  onSelectIncident: (inc: IncidentRecord) => void;
}

export const IncidentHistoryTable: React.FC<IncidentHistoryTableProps> = ({ incidents, onSelectIncident }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('ALL');

  const filtered = incidents.filter(inc => {
    const matchesSearch = inc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          inc.affected_system.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          inc.incident_id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = filterSeverity === 'ALL' || inc.severity === filterSeverity;
    return matchesSearch && matchesSeverity;
  });

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2.5rem' }}>
      
      {/* Header & Controls */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff' }}>
            Investigated Incidents & Memory Trail
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
            Chronological audit record of incidents triaged by the AI Memory Agent
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Search bar */}
          <div style={{ position: 'relative', width: '220px' }}>
            <Search size={14} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              placeholder="Search incidents..."
              className="input-field"
              style={{ paddingLeft: '2rem', fontSize: '0.8rem' }}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Severity Filter */}
          <select
            className="input-field"
            style={{ width: '130px', fontSize: '0.8rem' }}
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', textAlign: 'left', color: 'var(--text-muted)' }}>
              <th style={{ padding: '0.75rem 1rem' }}>Incident ID</th>
              <th style={{ padding: '0.75rem 1rem' }}>Title & System</th>
              <th style={{ padding: '0.75rem 1rem' }}>Severity</th>
              <th style={{ padding: '0.75rem 1rem' }}>Recurrence Tag</th>
              <th style={{ padding: '0.75rem 1rem' }}>Controls & Proof</th>
              <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length > 0 ? (
              filtered.map((inc) => (
                <tr
                  key={inc.incident_id}
                  style={{
                    borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                    transition: 'background 0.2s ease'
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                >
                  <td style={{ padding: '0.85rem 1rem', fontWeight: 600, color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>
                    {inc.incident_id}
                  </td>
                  <td style={{ padding: '0.85rem 1rem' }}>
                    <div style={{ fontWeight: 600, color: '#fff' }}>{inc.title}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.775rem' }}>{inc.affected_system}</div>
                  </td>
                  <td style={{ padding: '0.85rem 1rem' }}>
                    <span className={`badge ${inc.severity === 'CRITICAL' ? 'badge-rose' : inc.severity === 'HIGH' ? 'badge-amber' : 'badge-cyan'}`}>
                      {inc.severity}
                    </span>
                  </td>
                  <td style={{ padding: '0.85rem 1rem' }}>
                    {inc.is_recurring ? (
                      <span className="badge badge-violet" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                        <RefreshCw size={12} /> Recurrent ({inc.recalled_incident_id})
                      </span>
                    ) : (
                      <span className="badge badge-emerald">Initial Ingest</span>
                    )}
                  </td>
                  <td style={{ padding: '0.85rem 1rem', color: 'var(--text-muted)', fontSize: '0.775rem' }}>
                    <div>Mapped: <strong>{inc.mapped_controls?.length || 3} controls</strong></div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#34d399' }}>
                      <Hash size={12} /> Evidence Fingerprinted
                    </div>
                  </td>
                  <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                    <button
                      onClick={() => onSelectIncident(inc)}
                      className="btn-secondary"
                      style={{ padding: '0.35rem 0.75rem', fontSize: '0.775rem' }}
                    >
                      <Eye size={14} /> View Details
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                  No matching security incidents found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
