import React, { useState, useEffect } from 'react';
import { Search, Sparkles, Brain, Clock } from 'lucide-react';
import type { MemoryUnit, ReflectionInsight, TimelineEvent } from '../types/api';
import { apiService } from '../services/api';

export const MemoryExplorer: React.FC<{ initialNetwork?: string | null }> = ({ initialNetwork }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNetwork, setSelectedNetwork] = useState<string>(initialNetwork || 'all');
  const [memories, setMemories] = useState<MemoryUnit[]>([]);
  const [reflections, setReflections] = useState<ReflectionInsight[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [isReflecting, setIsReflecting] = useState(false);

  useEffect(() => {
    fetchMemories();
    fetchTimeline();
  }, [selectedNetwork]);

  const fetchMemories = async () => {
    try {
      const networkParam = selectedNetwork === 'all' ? undefined : selectedNetwork;
      const res = await apiService.recallMemories(searchQuery, networkParam);
      setMemories(res);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTimeline = async () => {
    try {
      const res = await apiService.getTimeline();
      setTimeline(res);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchMemories();
  };

  const handleReflect = async () => {
    setIsReflecting(true);
    try {
      const res = await apiService.reflectMemories();
      setReflections(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsReflecting(false);
    }
  };

  const getNetworkBadge = (net: string) => {
    switch (net) {
      case 'world': return <span className="badge badge-cyan">World Network</span>;
      case 'experience': return <span className="badge badge-violet">Experience Network</span>;
      case 'observation': return <span className="badge badge-emerald">Observation Network</span>;
      case 'opinion': return <span className="badge badge-amber">Opinion Network</span>;
      default: return <span className="badge badge-cyan">{net}</span>;
    }
  };

  return (
    <div style={{ marginBottom: '2.5rem' }}>
      
      {/* Search Header */}
      <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Brain size={20} color="#38bdf8" />
              Hybrid Semantic Memory Recall & Reflection Engine
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
              Search across structured security knowledge or synthesize strategic organizational insights.
            </p>
          </div>

          <button
            onClick={handleReflect}
            disabled={isReflecting}
            className="btn-primary"
            style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)' }}
          >
            <Sparkles size={16} />
            {isReflecting ? 'Reflecting Across Memories...' : 'Trigger Memory Reflection'}
          </button>
        </div>

        {/* Search & Filter Bar */}
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative', flex: 1, minWidth: '260px' }}>
            <Search size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              className="input-field"
              style={{ paddingLeft: '2.5rem' }}
              placeholder="Query memory bank (e.g. S3 ACL misconfiguration, SOC 2 CC6.1, access control)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {[
              { id: 'all', label: 'All Networks' },
              { id: 'world', label: 'World' },
              { id: 'experience', label: 'Experience' },
              { id: 'observation', label: 'Observation' },
              { id: 'opinion', label: 'Opinion' }
            ].map(net => (
              <button
                key={net.id}
                type="button"
                onClick={() => setSelectedNetwork(net.id)}
                style={{
                  background: selectedNetwork === net.id ? 'rgba(6, 182, 212, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                  border: selectedNetwork === net.id ? '1px solid #38bdf8' : '1px solid rgba(255, 255, 255, 0.1)',
                  color: selectedNetwork === net.id ? '#38bdf8' : 'var(--text-muted)',
                  padding: '0.5rem 0.85rem',
                  borderRadius: '8px',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  fontWeight: selectedNetwork === net.id ? 600 : 400
                }}
              >
                {net.label}
              </button>
            ))}
          </div>

          <button type="submit" className="btn-primary" style={{ padding: '0.5rem 1rem' }}>
            Recall
          </button>
        </form>
      </div>

      {/* Reflection Insights Output (if active) */}
      {reflections.length > 0 && (
        <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem', borderColor: 'rgba(217, 70, 239, 0.4)' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f0abfc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={18} color="#d946ef" /> Synthesized Memory Reflections & Risk Beliefs
          </h4>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {reflections.map((r, i) => (
              <div key={i} style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(217, 70, 239, 0.2)', borderRadius: '10px', padding: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <h5 style={{ fontSize: '0.9rem', color: '#fff', fontWeight: 600 }}>{r.title}</h5>
                  <span className="badge badge-rose">{r.impact_rating} IMPACT</span>
                </div>
                <p style={{ color: '#cbd5e1', fontSize: '0.825rem', marginBottom: '0.75rem', lineHeight: 1.4 }}>
                  {r.synthesis}
                </p>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                  <span>{r.evidence_count} Supporting Incidents</span>
                  {getNetworkBadge(r.network)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Grid: Memories & Timeline */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
        
        {/* Memory Units Cards */}
        <div>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#fff', marginBottom: '1rem' }}>
            Recalled Memory Units ({memories.length})
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {memories.length > 0 ? (
              memories.map((m) => (
                <div key={m.id} className="glass-panel" style={{ padding: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                      {getNetworkBadge(m.network)}
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>{m.id}</span>
                    </div>
                    <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 600 }}>
                      Confidence: {Math.round((m.cognitive_confidence || 0.95) * 100)}%
                    </span>
                  </div>

                  <h5 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.35rem' }}>
                    {m.title}
                  </h5>

                  <p style={{ color: '#cbd5e1', fontSize: '0.825rem', marginBottom: '0.75rem', lineHeight: 1.5 }}>
                    {m.content}
                  </p>

                  <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                    {m.tags.map((t, i) => (
                      <span key={i} style={{ background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '0.15rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem' }}>
                        #{t}
                      </span>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                No memory units found matching search query.
              </div>
            )}
          </div>
        </div>

        {/* Chronological Knowledge Stream */}
        <div>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Clock size={16} color="#38bdf8" /> Chronological Memory Stream
          </h4>

          <div className="glass-panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {timeline.map((item) => (
              <div key={item.id} style={{ borderLeft: '2px solid #38bdf8', paddingLeft: '0.75rem' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginBottom: '2px' }}>
                  {item.timestamp ? new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
                </div>
                <div style={{ fontSize: '0.8rem', color: '#e2e8f0', fontWeight: 500, lineHeight: 1.3 }}>
                  {item.summary}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
