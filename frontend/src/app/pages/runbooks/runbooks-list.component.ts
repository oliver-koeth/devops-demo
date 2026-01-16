import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { Runbook } from '../../models/runbook.model';
import { RunbooksService } from '../../services/runbooks.service';

interface RunbookFormState {
  title: string;
  tags: string;
  content: string;
}

@Component({
  selector: 'app-runbooks-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './runbooks-list.component.html'
})
export class RunbooksListComponent implements OnInit {
  runbooks: Runbook[] = [];
  filtered: Runbook[] = [];

  searchTerm = '';

  formState: RunbookFormState = {
    title: '',
    tags: '',
    content: ''
  };

  constructor(private runbooksService: RunbooksService, private router: Router) {}

  ngOnInit(): void {
    this.loadRunbooks();
  }

  loadRunbooks(): void {
    this.runbooks = this.runbooksService.getRunbooks();
    this.applyFilters();
  }

  applyFilters(): void {
    const term = this.searchTerm.trim().toLowerCase();
    this.filtered = this.runbooks.filter((runbook) => {
      if (!term) {
        return true;
      }
      return (
        runbook.title.toLowerCase().includes(term) ||
        runbook.tags.some((tag) => tag.toLowerCase().includes(term))
      );
    });
  }

  createRunbook(): void {
    if (!this.formState.title.trim() || !this.formState.content.trim()) {
      return;
    }
    const tags = this.formState.tags
      .split(',')
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0);
    const runbook = this.runbooksService.createRunbook({
      title: this.formState.title.trim(),
      tags,
      content: this.formState.content.trim()
    });
    this.formState = { title: '', tags: '', content: '' };
    this.loadRunbooks();
    void this.router.navigate(['/runbooks', runbook.id]);
  }

  deleteRunbook(id: string): void {
    const confirmDelete = window.confirm('Delete this runbook? This cannot be undone.');
    if (!confirmDelete) {
      return;
    }
    this.runbooksService.deleteRunbook(id);
    this.loadRunbooks();
  }
}
