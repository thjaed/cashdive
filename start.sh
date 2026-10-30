#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port 8000 &

cd /app/frontend
npm run start -- -p 3001 &

nginx -g "daemon off;"