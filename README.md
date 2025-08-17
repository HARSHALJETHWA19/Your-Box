# Drive (Local-first, production-grade scaffold)

This repo spins up a secure local environment:
- **Postgres 16**
- **MinIO** (S3-compatible)
- **Keycloak** (OIDC auth; ready to use with `drive` realm and `drive-web` client)
- **FastAPI backend** with JWT validation (via JWKS) and multipart pre-signed uploads to MinIO
- **Next.js** minimal UI with drag & drop + progress

## Prereqs
- Docker + Docker Compose
- Ports used: 3000 (web), 8080 (API), 8081 (Keycloak), 9000/9001 (MinIO)

## Quick start
```bash
cp .env.example .env
docker compose up -d --build
# MinIO console: http://localhost:9001  (user: minio / pass: minio123)
# Keycloak:      http://localhost:8081 (admin/admin) -> realm "drive"
# Web:           http://localhost:3000
# API:           http://localhost:8080/healthz
```
Create a bucket named **drive-local** in MinIO console before uploading.

## Security (local)
- OIDC JWT verification with JWKS (Keycloak). In this skeleton, upload endpoints are wired for auth dependency already; wire the token from the UI once you enable login UI.
- CORS locked to `WEB_ORIGIN`.
- DB connection pooling, pre-flight health checks.
- Pre-signed multipart upload (no data via backend).

## Next steps (local hardening)
- Add login UI (PKCE) using Keycloak's OIDC endpoints; attach `Authorization: Bearer <token>` on API calls.
- Implement quota checks, file listing, and share links.
- Add virus scanning worker and thumbnails (out-of-band) — see the AWS plan for Lambda equivalents.
