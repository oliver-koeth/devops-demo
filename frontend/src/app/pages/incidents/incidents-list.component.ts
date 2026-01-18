import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { Incident, IncidentSeverity, IncidentStatus } from '../../models/incident.model';
import { IncidentsService } from '../../services/incidents.service';

interface IncidentFormState {
  title: string;
  service: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
}

@Component({
  selector: 'app-incidents-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './incidents-list.component.html'
})
export class IncidentsListComponent implements OnInit {
  incidents: Incident[] = [];
  filtered: Incident[] = [];

  searchTerm = '';
  statusFilter: 'All' | IncidentStatus = 'All';
  severityFilter: 'All' | IncidentSeverity = 'All';

  formState: IncidentFormState = {
    title: '',
    service: '',
    severity: 'P2',
    status: 'Open'
  };

  constructor(private incidentsService: IncidentsService, private router: Router) {}

  ngOnInit(): void {
    this.loadIncidents();
  }

  loadIncidents(): void {
    this.incidentsService.getIncidents().subscribe((incidents) => {
      this.incidents = incidents;
      this.applyFilters();
    });
  }

  applyFilters(): void {
    const term = this.searchTerm.trim().toLowerCase();
    this.filtered = this.incidents.filter((incident) => {
      const matchesTerm =
        !term ||
        incident.title.toLowerCase().includes(term) ||
        incident.service.toLowerCase().includes(term);
      const matchesStatus = this.statusFilter === 'All' || incident.status === this.statusFilter;
      const matchesSeverity = this.severityFilter === 'All' || incident.severity === this.severityFilter;
      return matchesTerm && matchesStatus && matchesSeverity;
    });
  }

  createIncident(): void {
    if (!this.formState.title.trim() || !this.formState.service.trim()) {
      return;
    }
    this.incidentsService
      .createIncident({
        title: this.formState.title.trim(),
        service: this.formState.service.trim(),
        severity: this.formState.severity,
        status: this.formState.status
      })
      .subscribe((incident) => {
        this.formState = {
          title: '',
          service: '',
          severity: 'P2',
          status: 'Open'
        };
        this.loadIncidents();
        void this.router.navigate(['/incidents', incident.id]);
      });
  }

  resetFilters(): void {
    this.searchTerm = '';
    this.statusFilter = 'All';
    this.severityFilter = 'All';
    this.applyFilters();
  }

  deleteIncident(id: string): void {
    const confirmDelete = window.confirm('Delete this incident? This cannot be undone.');
    if (!confirmDelete) {
      return;
    }
    this.incidentsService.deleteIncident(id).subscribe(() => this.loadIncidents());
  }
}
