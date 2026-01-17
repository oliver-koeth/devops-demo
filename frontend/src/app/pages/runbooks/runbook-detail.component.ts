import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Runbook } from '../../models/runbook.model';
import { RunbooksService } from '../../services/runbooks.service';

interface RunbookEditState {
  title: string;
  tags: string;
  content: string;
}

@Component({
  selector: 'app-runbook-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './runbook-detail.component.html'
})
export class RunbookDetailComponent implements OnInit {
  runbook?: Runbook;
  editState?: RunbookEditState;

  constructor(private runbooksService: RunbooksService, private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      return;
    }
    this.loadRunbook(id);
  }

  loadRunbook(id: string): void {
    this.runbook = this.runbooksService.getRunbookById(id);
    if (this.runbook) {
      this.editState = {
        title: this.runbook.title,
        tags: this.runbook.tags.join(', '),
        content: this.runbook.content
      };
    }
  }

  saveChanges(): void {
    if (!this.runbook || !this.editState) {
      return;
    }
    if (!this.editState.title.trim() || !this.editState.content.trim()) {
      return;
    }
    const tags = this.editState.tags
      .split(',')
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0);
    const updated = this.runbooksService.updateRunbook(this.runbook.id, {
      title: this.editState.title.trim(),
      tags,
      content: this.editState.content.trim()
    });
    if (updated) {
      this.runbook = updated;
      if (this.editState) {
        this.editState.tags = updated.tags.join(', ');
      }
    }
  }

  deleteRunbook(): void {
    if (!this.runbook) {
      return;
    }
    const confirmDelete = window.confirm('Delete this runbook? This cannot be undone.');
    if (!confirmDelete) {
      return;
    }
    this.runbooksService.deleteRunbook(this.runbook.id);
    void this.router.navigate(['/runbooks']);
  }
}
