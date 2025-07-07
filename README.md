# Medic

This project contains a tiny example with a simple Node.js backend and a small HTML frontend.

## Backend

The backend is a minimal Node.js HTTP server. It exposes `/api/status` which returns `{ "status": "ok" }` and also serves the files in the `frontend` directory.

### Running

```bash
node backend/server.js
```

## Frontend

Once the server is running, open [http://localhost:3000](http://localhost:3000) in your browser. The page will query the backend on load and display its status.

## Agent Notes

This repository includes an `AGENTS.md` file with guidelines for automated
contributors. Any future improvements should follow those instructions and keep
the project lightweight.
