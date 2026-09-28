export type MemoryNetworkType = 'world' | 'experience' | 'observation' | 'opinion';

export interface MemoryNetworkCounts {
  world: number;
  experience: number;
  observation: number;
  opinion: number;
}

export interface SystemHealth {
  status: string;
  service: string;
  memory_backend: string;
  networks_status: {
    bank_id: string;
    engine_mode: string;
    networks: MemoryNetworkCounts;
    total_memories: number;
  };
  llm_engine: string;
}

export interface SecurityControl {
  framework: string; // e.g. "SOC 2", "NIST CSF", "ISO 27001"
  control_id: string; // e.g. "CC6.1"
  name: string;
  status: 'COMPLIANT' | 'NON_COMPLIANT' | 'REMEDIATED';
  description: string;
}

export interface EvidenceFingerprint {
  evidence_id: string;
  type: string;
  sha256_hash: string;
  timestamp: string;
  verified: boolean;
}

export interface IncidentRequest {
  title: string;
  affected_system: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  logs?: string;
  vector?: string;
}

export interface IncidentRecord {
  incident_id: string;
  title: string;
  affected_system: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  status: 'INVESTIGATED' | 'REMEDIATED' | 'CLOSED';
  root_cause: string;
  vector: string;
  mapped_controls: SecurityControl[];
  evidence_fingerprints: EvidenceFingerprint[];
  remediation_playbook: string[];
  is_recurring: boolean;
  recalled_incident_id?: string;
  similarity_score?: number;
  timestamp: string;
}

export interface MemoryUnit {
  id: string;
  network: MemoryNetworkType;
  title: string;
  content: string;
  cognitive_confidence: number;
  tags: string[];
  created_at: string;
}

export interface ReflectionInsight {
  network: MemoryNetworkType;
  title: string;
  synthesis: string;
  evidence_count: number;
  impact_rating: string;
}

export interface AuditQueryRequest {
  category: string;
  question: string;
}

export interface AuditQueryResult {
  query_id: string;
  category: string;
  question: string;
  compliance_status: 'COMPLIANT_WITH_EVIDENCE' | 'NON_COMPLIANT' | 'REMEDIATION_REQUIRED';
  audit_findings: string[];
  evidence_hashes: string[];
  guidance: string;
  timestamp: string;
}

export interface TimelineEvent {
  id: string;
  timestamp: string;
  event_type: 'INCIDENT_INGEST' | 'RCA_COMPLETED' | 'MEMORY_RETAINED' | 'RECURRENCE_RECALLED' | 'AUDIT_QUERY';
  network?: MemoryNetworkType;
  summary: string;
}

export interface DemoStep {
  step_number: number;
  title: string;
  description: string;
  action_type: string;
  result: string;
  memory_impact: string;
}
