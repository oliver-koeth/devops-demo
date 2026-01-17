import { Injectable } from '@angular/core';

import { Incident, IncidentNote, IncidentSeverity, IncidentStatus } from '../models/incident.model';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class IncidentsService {
  constructor(private storage: StorageService) {}

  getIncidents(): Incident[] {
    return [...this.storage.getData().incidents].sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  }

  getIncidentById(id: string): Incident | undefined {
    return this.storage.getData().incidents.find((incident) => incident.id === id);
  }

  createIncident(input: {
    title: string;
    severity: IncidentSeverity;
    status: IncidentStatus;
    service: string;
  }): Incident {
    const data = this.storage.getData();
    const timestamp = new Date().toISOString();
    const incident: Incident = {
      id: crypto.randomUUID(),
      title: input.title,
      severity: input.severity,
      status: input.status,
      service: input.service,
      createdAt: timestamp,
      updatedAt: timestamp,
      notes: []
    };
    data.incidents.unshift(incident);
    this.storage.setData(data);
    return incident;
  }

  updateIncident(id: string, updates: Partial<Omit<Incident, 'id' | 'createdAt' | 'notes'>>): Incident | undefined {
    const data = this.storage.getData();
    const index = data.incidents.findIndex((incident) => incident.id === id);
    if (index === -1) {
      return undefined;
    }
    const updated: Incident = {
      ...data.incidents[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    data.incidents[index] = updated;
    this.storage.setData(data);
    return updated;
  }

  addNote(id: string, note: Omit<IncidentNote, 'timestamp'>): Incident | undefined {
    const data = this.storage.getData();
    const incident = data.incidents.find((entry) => entry.id === id);
    if (!incident) {
      return undefined;
    }
    incident.notes.unshift({
      ...note,
      timestamp: new Date().toISOString()
    });
    incident.updatedAt = new Date().toISOString();
    this.storage.setData(data);
    return incident;
  }

  toggleStatus(id: string): Incident | undefined {
    const incident = this.getIncidentById(id);
    if (!incident) {
      return undefined;
    }
    return this.updateIncident(id, {
      status: incident.status === 'Open' ? 'Closed' : 'Open'
    });
  }

  deleteIncident(id: string): void {
    const data = this.storage.getData();
    data.incidents = data.incidents.filter((incident) => incident.id !== id);
    this.storage.setData(data);
  }
}
