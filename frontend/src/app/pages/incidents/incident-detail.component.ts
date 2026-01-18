import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Incident, IncidentNote, IncidentSeverity, IncidentStatus } from '../../models/incident.model';
import { IncidentsService } from '../../services/incidents.service';

interface IncidentEditState {
  title: string;
  service: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
}

@Component({
  selector: 'app-incident-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './incident-detail.component.html'
})
export class IncidentDetailComponent implements OnInit {
  incident?: Incident;
  editState?: IncidentEditState;
  noteAuthor = '';
  noteText = '';

  constructor(
    private incidentsService: IncidentsService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      return;
    }
    this.loadIncident(id);
  }

  loadIncident(id: string): void {
    this.incidentsService.getIncidentById(id).subscribe({
      next: (incident) => {
        this.incident = incident;
        this.editState = {
          title: incident.title,
          service: incident.service,
          severity: incident.severity,
          status: incident.status
        };
      },
      error: () => {
        this.incident = undefined;
        this.editState = undefined;
      }
    });
  }

  saveChanges(): void {
    if (!this.incident || !this.editState) {
      return;
    }
    if (!this.editState.title.trim() || !this.editState.service.trim()) {
      return;
    }
    this.incidentsService
      .updateIncident(this.incident.id, {
        title: this.editState.title.trim(),
        service: this.editState.service.trim(),
        severity: this.editState.severity,
        status: this.editState.status
      })
      .subscribe((updated) => {
        this.incident = updated;
      });
  }

  toggleStatus(): void {
    if (!this.incident) {
      return;
    }
    this.incidentsService.toggleStatus(this.incident.id, this.incident.status).subscribe((updated) => {
      this.incident = updated;
      if (this.editState) {
        this.editState.status = updated.status;
      }
    });
  }

  addNote(): void {
    if (!this.incident || !this.noteAuthor.trim() || !this.noteText.trim()) {
      return;
    }
    this.incidentsService
      .addNote(this.incident.id, {
        author: this.noteAuthor.trim(),
        text: this.noteText.trim()
      })
      .subscribe((updated) => {
        this.incident = updated;
        this.noteAuthor = '';
        this.noteText = '';
      });
  }

  deleteIncident(): void {
    if (!this.incident) {
      return;
    }
    const confirmDelete = window.confirm('Delete this incident? This cannot be undone.');
    if (!confirmDelete) {
      return;
    }
    this.incidentsService.deleteIncident(this.incident.id).subscribe(() => {
      void this.router.navigate(['/incidents']);
    });
  }

  trackByTimestamp(_: number, note: IncidentNote): string {
    return note.timestamp;
  }
}
