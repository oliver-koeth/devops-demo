# Stage 1 Codex Prompt (Environment)

## Role & Scope

You are acting as a senior full-stack engineer preparing the initial repository for a staged demo application for a DevOps audience.

The application will be built incrementally in later steps.  
In this step, you must **only** initialize the project environment and repository structure.  
Do **not** implement any application logic, UI screens, backend APIs, or MCP server functionality yet.

---

## High-level Project Intent  
*(for context only — do not implement yet)*

- Web application demo for a DevOps team  
- Frontend: modern Angular (not AngularJS 1.x)  
- Initial persistence: browser local storage  
- Later backend: Python service persisting to the filesystem  
- Later integrations:
  - MCP server exposing search over incidents  
  - Native ChatGPT app via MCP with UI resources  

This context is provided to influence **structure and documentation only**.

---

## Your Task in This Step

Initialize the repository with:

1. **A clear, professional `README.md`** that:
   - Explains the purpose of the project  
   - Describes the staged roadmap (without implementation)  
   - Clearly states what is in scope and out of scope for the current stage  

2. **An appropriate open-source license file**  
   - Use Apache License 2.0 unless there is a strong reason not to  

3. **A clean repository folder structure** that anticipates:
   - `frontend/` — Angular app  
   - `backend/` — Python service (added later)  
   - `mcp/` — MCP server code (added later)  
   - `docs/` — architecture notes, prompting strategy, demo scripts  

   Do **not** scaffold Angular or Python projects yet.  
   Only create folders and placeholder files if helpful.

4. **A lightweight agent / contribution guidance file**  
   (e.g. `AGENTS.md` or `CONTRIBUTING.md`) that:
   - Explains how future AI agents (e.g. Codex) should work in small, incremental steps  
   - Emphasizes not implementing future stages prematurely  

5. **Any minimal config files** you consider essential at repo start  
   (e.g. `.gitignore`)

---

## Constraints

- Do **not** generate application code  
- Do **not** scaffold Angular or Python projects yet  
- Do **not** add MCP server code  
- Focus on clarity, maintainability, and future extensibility  
- Keep everything minimal but professional  

---

## Output Format

- Show the directory tree  
- Then provide the full contents of each file you created  

---
