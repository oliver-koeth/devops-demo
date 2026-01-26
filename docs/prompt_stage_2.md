# Stage 2 Codex Prompt (Frontend)

## Role & Context

You are acting as a senior Angular engineer building **Stage 2** of a staged demo application.

**Context (do not implement future stages yet):**
- Stage 3 will add a Python backend and remove `localStorage`.
- Stage 4/5 will add an MCP server and ChatGPT-native integration.

This context is **only** to influence architecture choices and naming.

---

## Scope for This Step

Implement **only** the frontend MVP as a standalone Angular web application with local persistence.

- Use the latest stable Angular version available via Angular CLI at build time.
- Data must persist in browser `localStorage`.
- No backend server, no MCP server code, no Docker, no deployment scripts.

---

## Functional Requirements

The application is a **DevOps Runbook Assistant** MVP with two core entities.

### Incidents
- Fields: `id` (string), `title`, `severity` (P1–P4), `status` (Open/Closed), `service`,
  `createdAt` (ISO string), `updatedAt` (ISO string), `notes[]`.
- Notes fields: `timestamp` (ISO string), `author`, `text`.
- UI requirements:
  - Incidents list view with search (title/service) and filters (status, severity).
  - Incident detail view showing metadata and a timeline of notes.
  - Ability to create, edit, add notes, close/reopen, and delete incidents.

### Runbooks
- Fields: `id` (string), `title`, `tags[]` (string), `content` (markdown or plain text),
  `createdAt`, `updatedAt`.
- UI requirements:
  - Runbooks list view with search (title/tags).
  - Runbook detail view.
  - Ability to create, edit, and delete runbooks.

### Navigation
- Top-level navigation for Incidents and Runbooks.
- Deep links for detail pages (`/incidents/:id`, `/runbooks/:id`).
- Empty-state pages when no data exists.

### Seed Data
- On first launch (when no `localStorage` data exists), initialize:
  - 2–3 sample incidents
  - 2 sample runbooks

### UX Expectations
- Clean, professional UI (no fancy styling required).
- Basic form validation and user feedback (e.g. required fields).
- Prefer Angular built-in features and minimal dependencies.

---

## Architecture Requirements

- Follow strict TypeScript and Angular best practices.
- Use standalone components and the Angular router.
- Implement a small data-access layer:
  - A storage service that wraps `localStorage` (get/set, schema version, safe parsing).
  - Repository/services for incidents and runbooks.
  - All write operations must update `updatedAt` timestamps.
- Include a lightweight `schemaVersion` key in `localStorage` to allow future migrations (Stage 3).

---

## Testing Requirements

Use **Playwright end-to-end tests** (this is important).

- Add Playwright to the repository and create a minimal test suite:
  1. Can create an incident and see it in list and detail views.
  2. Incident data persists after a page reload (`localStorage`).
  3. Can create a runbook and see it after reload.
- Keep tests stable by using `data-testid` attributes for key elements.

Do **not** set up component testing.  
Do **not** require a backend for tests.

---

## Repo Hygiene

- Update `README.md` to reflect Stage 2 status, including:
  - How to run the app
  - How to run tests
- Update `AGENTS.md` / `CONTRIBUTING.md` to explain the staged approach and how to extend in Stage 3+.
- Add or extend `.gitignore` as appropriate.
- Ensure the following commands work:
  - `npm install`
  - `npm run build`
  - `npm test` (or documented equivalents)

---

## Deliverables

1. Generate the Angular project under `frontend/`.
2. Provide a directory tree of `frontend/` and list any modified root-level files
   (e.g. `README.md`, `AGENTS.md`).
3. Provide concise run instructions (commands) for:
   - Starting the development server
   - Running Playwright tests
   - Building the production bundle

---

## Important Constraints

- Do **not** create any backend code.
- Do **not** create any MCP server code.
- Do **not** overengineer state management (no NgRx unless truly necessary).
- Keep dependencies minimal.
