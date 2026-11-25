---
name: web-ts
description: Stack notes for web/TypeScript work - React/Next-style frontends, Supabase (SQL, RLS, edge functions), Vercel, and how CI should be set up for JS/TS repos. Load before writing, testing, or setting up CI for web/TS code.
---

# Web / TypeScript

Project conventions (CLAUDE.md/AGENTS.md, existing code, package manager lockfile) win over anything here.

## Code
- Strict TypeScript; no `any` without a reason. Validate data at boundaries (API responses, forms, env).
- Use the project's existing UI library, styling approach, data fetching, and state patterns; don't add a new one.
- Accessibility: semantic elements, labels on inputs, keyboard reachable, visible focus.
- Use the package manager the lockfile says (pnpm/npm/yarn/bun).

## Supabase
- Every new table gets RLS enabled with explicit policies; test policies as the anon and authenticated roles.
- Schema changes go in migration files, never ad-hoc against the hosted project. Local (`supabase start`) or dev only, unless the task explicitly says otherwise.
- Service-role keys never reach the client or the repo.

## Vercel
- Env vars per environment; never commit `.env*` with real values. Deploys only through devops with the owner's approval.

## CI for JS/TS repos (when setting up or changing CI)
- Fast typecheck (`tsgo` instead of `tsc`) if the project supports it.
- oxlint with as many rules enabled as practical.
- Test shards balanced by recorded test time.
- PRs run only tests affected by the diff.
- Lint, typecheck, build, and tests as parallel jobs.

## Running checks
- A hook puts a time limit on npm/pnpm/test/build commands: it hands you a wrapped command that writes output to a log; run that. On TIMED OUT, report it. Dev servers started in the background also get a limit: add `# timeout=4h` to the command if it must stay up.
