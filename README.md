# Stat Checker

This repository is the scaffold for a research-paper statistical consistency checker: a FastAPI backend, a Next.js frontend, and a Python pipeline for PDF extraction plus statcheck/GRIM/SPRITE-style consistency checks. To run the local stack, start Docker and use `docker-compose up`; then verify the backend at `http://localhost:8000/health`, Postgres on `localhost:5432`, and GROBID at `http://localhost:8070/api/isalive`.
