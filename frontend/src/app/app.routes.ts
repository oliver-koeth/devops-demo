import { Routes } from '@angular/router';
import { IncidentsListComponent } from './pages/incidents/incidents-list.component';
import { IncidentDetailComponent } from './pages/incidents/incident-detail.component';
import { RunbooksListComponent } from './pages/runbooks/runbooks-list.component';
import { RunbookDetailComponent } from './pages/runbooks/runbook-detail.component';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'incidents' },
  { path: 'incidents', component: IncidentsListComponent },
  { path: 'incidents/:id', component: IncidentDetailComponent },
  { path: 'runbooks', component: RunbooksListComponent },
  { path: 'runbooks/:id', component: RunbookDetailComponent },
  { path: '**', redirectTo: 'incidents' }
];
