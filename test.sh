#!/bin/sh
set -e
node backend/server.js &
SERVER_PID=$!
# Give the server a moment to start
sleep 1
curl -s http://localhost:3000/api/status
curl -s http://localhost:3000/
kill $SERVER_PID
