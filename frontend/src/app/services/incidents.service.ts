import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../config/api.config';
import { Incident, IncidentNote, IncidentSeverity, IncidentStatus } from '../models/incident.model';

@Injectable({
  providedIn: 'root'
})
export class IncidentsService {
  constructor(private http: HttpClient) {}

  getIncidents(): Observable<Incident[]> {
    return this.http.get<Incident[]>(`${API_BASE_URL}/incidents`);
  }

  getIncidentById(id: string): Observable<Incident> {
    return this.http.get<Incident>(`${API_BASE_URL}/incidents/${id}`);
  }

  createIncident(input: {
    title: string;
    severity: IncidentSeverity;
    status: IncidentStatus;
    service: string;
  }): Observable<Incident> {
    return this.http.post<Incident>(`${API_BASE_URL}/incidents`, input);
  }

  updateIncident(
    id: string,
    updates: Partial<Omit<Incident, 'id' | 'createdAt' | 'notes'>>
  ): Observable<Incident> {
    return this.http.put<Incident>(`${API_BASE_URL}/incidents/${id}`, updates);
  }

  addNote(id: string, note: Omit<IncidentNote, 'timestamp'>): Observable<Incident> {
    return this.http.post<Incident>(`${API_BASE_URL}/incidents/${id}/notes`, note);
  }

  toggleStatus(id: string, currentStatus: IncidentStatus): Observable<Incident> {
    const action = currentStatus === 'Open' ? 'close' : 'reopen';
    return this.http.post<Incident>(`${API_BASE_URL}/incidents/${id}/${action}`, {});
  }

  deleteIncident(id: string): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/incidents/${id}`);
  }
}
