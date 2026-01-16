import { Injectable } from '@angular/core';

import { Runbook } from '../models/runbook.model';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root'
})
export class RunbooksService {
  constructor(private storage: StorageService) {}

  getRunbooks(): Runbook[] {
    return [...this.storage.getData().runbooks].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
  }

  getRunbookById(id: string): Runbook | undefined {
    return this.storage.getData().runbooks.find((runbook) => runbook.id === id);
  }

  createRunbook(input: { title: string; tags: string[]; content: string }): Runbook {
    const data = this.storage.getData();
    const timestamp = new Date().toISOString();
    const runbook: Runbook = {
      id: crypto.randomUUID(),
      title: input.title,
      tags: input.tags,
      content: input.content,
      createdAt: timestamp,
      updatedAt: timestamp
    };
    data.runbooks.unshift(runbook);
    this.storage.setData(data);
    return runbook;
  }

  updateRunbook(id: string, updates: Partial<Omit<Runbook, 'id' | 'createdAt'>>): Runbook | undefined {
    const data = this.storage.getData();
    const index = data.runbooks.findIndex((runbook) => runbook.id === id);
    if (index === -1) {
      return undefined;
    }
    const updated: Runbook = {
      ...data.runbooks[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    data.runbooks[index] = updated;
    this.storage.setData(data);
    return updated;
  }

  deleteRunbook(id: string): void {
    const data = this.storage.getData();
    data.runbooks = data.runbooks.filter((runbook) => runbook.id !== id);
    this.storage.setData(data);
  }
}
