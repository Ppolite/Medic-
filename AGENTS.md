# Agent Instructions

This repository contains a tiny Node.js backend and a small HTML frontend. When updating the code, keep these guidelines in mind:

1. Use only built-in Node.js modules if possible.
2. After making changes, ensure the server still starts and the frontend can reach `/api/status`.
3. Verify functionality using the provided `test.sh` script or by running:
   ```bash
   node backend/server.js &
   curl http://localhost:3000/api/status
   curl http://localhost:3000/
   ```
   The status endpoint should return `{"status":"ok"}` and the homepage should serve the HTML page.
4. Keep the README concise and maintain a minimal approach.
5. Aim to gradually improve the codebase over time while keeping dependencies minimal.
