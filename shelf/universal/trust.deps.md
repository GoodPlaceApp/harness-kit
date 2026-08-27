# `trust.deps` — How are dependencies chosen, updated and vetted before adoption?

```yaml
slot: trust.deps
title: A stated admission test for new dependencies, and a routine that keeps them current
statement: >
  A new dependency is admitted only after a stated check: it is maintained, its licence is
  compatible with the project's, its transitive weight is understood, and the work it saves
  exceeds the cost of carrying it. Versions are pinned in a committed lockfile. Updates
  arrive on a routine — automated proposals reviewed in batches — rather than only when
  something breaks, so the project never faces a multi-year upgrade under incident pressure.
rationale: >
  Dependencies are the largest attack surface most projects have and the one most often
  adopted without a decision. Pinning without a refresh routine converts a security problem
  into a slower security problem: the version stops moving but the vulnerabilities do not.
tier: S
evidence: documented
corroboration: 3
check: "ls package-lock.json yarn.lock pnpm-lock.yaml requirements.lock.txt poetry.lock Cargo.lock go.sum gradle.lockfile 2>/dev/null | head -1"
```

**Recipes** — automated update proposals: Dependabot or Renovate (any stack, via the code
host) · `pip-audit` / `safety` (Python) · `npm audit` / `osv-scanner` (JavaScript) ·
`cargo audit` (Rust) · `govulncheck` (Go). Licence compatibility: `pip-licenses`,
`license-checker`, `cargo-deny`.

**Sources** — OWASP SAMM, Implementation → Secure Build and Operations → Environment
Management; the OpenSSF Scorecard checks, which score dependency-update automation and
pinning as distinct properties.
