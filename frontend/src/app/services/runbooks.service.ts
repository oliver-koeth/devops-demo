import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../config/api.config';
import { Runbook } from '../models/runbook.model';

@Injectable({
  providedIn: 'root'
})
export class RunbooksService {
  constructor(private http: HttpClient) {}

  getRunbooks(): Observable<Runbook[]> {
    return this.http.get<Runbook[]>(`${API_BASE_URL}/runbooks`);
  }

  getRunbookById(id: string): Observable<Runbook> {
    return this.http.get<Runbook>(`${API_BASE_URL}/runbooks/${id}`);
  }

  createRunbook(input: { title: string; tags: string[]; content: string }): Observable<Runbook> {
    return this.http.post<Runbook>(`${API_BASE_URL}/runbooks`, input);
  }

  updateRunbook(
    id: string,
    updates: Partial<Omit<Runbook, 'id' | 'createdAt'>>
  ): Observable<Runbook> {
    return this.http.put<Runbook>(`${API_BASE_URL}/runbooks/${id}`, updates);
  }

  deleteRunbook(id: string): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/runbooks/${id}`);
  }
}
