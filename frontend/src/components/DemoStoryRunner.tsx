import React, { useState } from 'react';
import { Play, RefreshCw, Terminal } from 'lucide-react';
import type { DemoStep } from '../types/api';
import { apiService } from '../services/api';

export const DemoStoryRunner: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(-1);
  const [steps, setSteps] = useState<DemoStep[]>([]);

  const handleRunStory = async () => {
    setIsRunning(true);
    setCurrentStepIndex(0);

    try {
      const res = await apiService.runDemoStory();
      setSteps(res.steps);

      // Play through steps with timing animation
      for (let i = 0; i < res.steps.length; i++) {
        setCurrentStepIndex(i);
        await new Promise(r => setTimeout(r, 650));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2.5rem' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Terminal size={20} color="#38bdf8" />
            10-Step Automated Storyline Player
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem' }}>
            Demonstrates the complete end-to-end memory loop: Incident Ingest → RCA → Control Mapping → Hindsight Retention → Recurrence Recall → Audit Inquiry Answering.
          </p>
        </div>

        <button
          onClick={handleRunStory}
          disabled={isRunning}
          className="btn-primary"
          style={{ background: 'linear-gradient(135deg, #10b981 0%, #0ea5e9 100%)', padding: '0.65rem 1.5rem' }}
        >
          {isRunning ? (
            <>
              <RefreshCw size={18} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
              Executing Step {currentStepIndex + 1} of 10...
            </>
          ) : (
            <>
              <Play size={18} /> Run Automated 10-Step Demo Story
            </>
          )}
        </button>
      </div>

      {/* Steps List */}
      {steps.length > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {steps.map((step, idx) => {
            const isActive = idx === currentStepIndex;
            const isCompleted = idx <= currentStepIndex;

            return (
              <div
                key={step.step_number}
                style={{
                  background: isActive
                    ? 'linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%)'
                    : isCompleted
                    ? 'rgba(15, 23, 42, 0.6)'
                    : 'rgba(15, 23, 42, 0.3)',
                  border: isActive
                    ? '1px solid #38bdf8'
                    : isCompleted
                    ? '1px solid rgba(255, 255, 255, 0.08)'
                    : '1px dashed rgba(255, 255, 255, 0.05)',
                  borderRadius: '10px',
                  padding: '1rem',
                  transition: 'all 0.3s ease',
                  opacity: isCompleted ? 1 : 0.4
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: '50%',
                      background: isCompleted ? 'linear-gradient(135deg, #0ea5e9, #6366f1)' : 'rgba(255, 255, 255, 0.1)',
                      color: '#fff',
                      fontWeight: 700,
                      fontSize: '0.8rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      {step.step_number}
                    </div>

                    <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: isActive ? '#38bdf8' : '#fff' }}>
                      {step.title}
                    </h4>
                  </div>

                  <span className="badge badge-cyan" style={{ fontSize: '0.65rem' }}>
                    {step.action_type}
                  </span>
                </div>

                <p style={{ color: '#cbd5e1', fontSize: '0.825rem', marginLeft: '2.5rem', marginBottom: '0.5rem' }}>
                  {step.description}
                </p>

                <div style={{ marginLeft: '2.5rem', display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.75rem' }}>
                  <span style={{ color: '#34d399', fontWeight: 500 }}>
                    <strong>Result:</strong> {step.result}
                  </span>
                  <span style={{ color: '#c084fc' }}>
                    <strong>Memory Loop:</strong> {step.memory_impact}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '3rem 1.5rem', background: 'rgba(15, 23, 42, 0.4)', borderRadius: '12px', color: 'var(--text-muted)' }}>
          <Play size={40} color="#64748b" style={{ marginBottom: '0.75rem' }} />
          <h4 style={{ color: '#94a3b8', fontSize: '1rem', marginBottom: '0.35rem' }}>Ready to Execute Demo Story</h4>
          <p style={{ fontSize: '0.825rem', maxWidth: '380px', margin: '0 auto' }}>
            Click "Run Automated 10-Step Demo Story" above to watch the agent triage Incident #1024, retain memory, recall on Incident #1038, and generate an audit package.
          </p>
        </div>
      )}

    </div>
  );
};
