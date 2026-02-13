# MultiNegocios AI SaaS

Multi-tenant AI SaaS for processing commercial messages into structured product data.

## Tech Stack

- FastAPI (async)
- PostgreSQL (async)
- SQLAlchemy 2.0
- Alembic
- JWT Authentication
- Tenant Isolation Middleware
- CrewAI Processing Pipeline
- Decimal-safe financial handling

## Architecture Evolution

### Block 1
Async infrastructure + PostgreSQL

### Block 2
Multi-tenant JWT middleware

### Block 3
Security validation + auth hardening

### Block 4
CrewAI structured pipeline (regex-first, optional LLM fallback)

## Current Status

Core infrastructure and AI pipeline implemented.  
Next step: Async persistence endpoint with tenant isolation.
