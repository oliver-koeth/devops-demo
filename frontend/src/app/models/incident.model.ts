export type IncidentSeverity = 'P1' | 'P2' | 'P3' | 'P4';
export type IncidentStatus = 'Open' | 'Closed';

export interface IncidentNote {
  timestamp: string;
  author: string;
  text: string;
}

export interface Incident {
  id: string;
  title: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  service: string;
  createdAt: string;
  updatedAt: string;
  notes: IncidentNote[];
}
