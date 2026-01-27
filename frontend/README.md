# Frontend (Angular)

## Overview
The frontend is a standalone Angular web app for managing incidents and runbooks. It talks to the backend REST API and provides the human-facing UI.

## Prerequisites
- Node.js and npm
- Backend API running at `http://localhost:8000` (used by the dev server)

## Install Dependencies
```bash
cd frontend
npm install
```

## Run (Dev Server)
```bash
cd frontend
npm run start
```
The app will be available at `http://localhost:4200` and will call the backend at `http://localhost:8000/api/v1`.

## Build
```bash
cd frontend
npm run build
```

## Test (Playwright)
```bash
cd frontend
npm run test
```
