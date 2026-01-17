import { Injectable } from '@angular/core';

import { Incident } from '../models/incident.model';
import { Runbook } from '../models/runbook.model';

export interface AppStorage {
  schemaVersion: number;
  incidents: Incident[];
  runbooks: Runbook[];
}

@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private readonly storageKey = 'devops-runbook-assistant';
  private readonly schemaVersion = 1;

  getData(): AppStorage {
    const raw = localStorage.getItem(this.storageKey);
    if (!raw) {
      const seeded = this.seedData();
      this.setData(seeded);
      return seeded;
    }

    try {
      const parsed = JSON.parse(raw) as AppStorage;
      if (!parsed || parsed.schemaVersion !== this.schemaVersion) {
        const seeded = this.seedData();
        this.setData(seeded);
        return seeded;
      }
      return parsed;
    } catch (error) {
      const seeded = this.seedData();
      this.setData(seeded);
      return seeded;
    }
  }

  setData(data: AppStorage): void {
    localStorage.setItem(this.storageKey, JSON.stringify(data));
  }

  private seedData(): AppStorage {
    const now = new Date();
    const incidentCreated = new Date(now.getTime() - 1000 * 60 * 60 * 5).toISOString();
    const incidentUpdated = new Date(now.getTime() - 1000 * 60 * 60 * 2).toISOString();
    const secondaryCreated = new Date(now.getTime() - 1000 * 60 * 60 * 24).toISOString();

    return {
      schemaVersion: this.schemaVersion,
      incidents: [
        {
          id: crypto.randomUUID(),
          title: 'Checkout latency spikes in us-east-1',
          severity: 'P1',
          status: 'Open',
          service: 'Payments API',
          createdAt: incidentCreated,
          updatedAt: incidentUpdated,
          notes: [
            {
              timestamp: incidentCreated,
              author: 'On-call Bot',
              text: 'Pager triggered for elevated latency. Investigating recent deploy.'
            },
            {
              timestamp: incidentUpdated,
              author: 'A. Rivera',
              text: 'Rolled back to 2024.08.12 build; seeing partial recovery.'
            }
          ]
        },
        {
          id: crypto.randomUUID(),
          title: 'CI queue backlog for staging',
          severity: 'P3',
          status: 'Closed',
          service: 'CI Orchestrator',
          createdAt: secondaryCreated,
          updatedAt: secondaryCreated,
          notes: [
            {
              timestamp: secondaryCreated,
              author: 'L. Chen',
              text: 'Scaled runners and cleared backlog. Monitoring for recurrence.'
            }
          ]
        }
      ],
      runbooks: [
        {
          id: crypto.randomUUID(),
          title: 'Database failover checklist',
          tags: ['database', 'failover', 'postgres'],
          content: '1. Confirm replica health\n2. Pause write-heavy jobs\n3. Promote replica\n4. Validate app connectivity',
          createdAt: secondaryCreated,
          updatedAt: secondaryCreated
        },
        {
          id: crypto.randomUUID(),
          title: 'Cache eviction response',
          tags: ['cache', 'redis'],
          content: 'If cache eviction storms occur:\n- Increase memory threshold\n- Review key TTLs\n- Enable lazy freeing',
          createdAt: incidentCreated,
          updatedAt: incidentCreated
        }
      ]
    };
  }
}
