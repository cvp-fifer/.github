# Security Policy

This policy applies org-wide to every repository under
[`cvp-fifer`](https://github.com/cvp-fifer) unless a repository ships its
own `SECURITY.md`, which then takes precedence for that repository.

## Reporting a vulnerability

Please **do not** open a public issue, pull request, or discussion for
anything security-sensitive.

Report privately through **GitHub's private vulnerability reporting**:

1. Go to the affected repository's **Security** tab.
2. Choose **Report a vulnerability** (under *Advisories*).
3. Fill in the advisory form.

This opens a private channel visible only to you and the maintainers. If
private reporting is not enabled on a given repository, or you cannot
reach it, contact a maintainer privately and ask them to open an advisory
on your behalf — do not post details in any public location.

### Preferred report contents

- A description of the issue and its impact.
- Steps to reproduce (proof-of-concept where possible).
- Affected versions, or the commit SHA if reporting against `main`.
- Environment: OS, architecture, and any relevant toolchain/runtime
  versions.
- Any known workaround.
- Your preferred attribution (name, handle, or anonymous) once a fix
  ships.

## Coordinated disclosure

We follow a **90-day coordinated disclosure embargo** by default, counted
from the date a maintainer acknowledges the report. Extensions are
possible by mutual agreement. We aim to acknowledge new reports within a
few business days. Public disclosure ahead of a fix is a last resort,
reserved for cases where the embargo has lapsed without remediation.

Reporters who follow coordinated disclosure are credited (with their
permission) in the release notes once a fix has shipped.

## Supported versions

Fifer products are pre-1.0. Only the latest released line receives
security fixes.

| Version            | Supported |
| ------------------ | --------- |
| pre-1.0 — latest   | Yes       |
| pre-1.0 — older    | No        |

Post-1.0, this table will expand to cover the most recent minor release
line and the one before it (N and N-1).

## Scope

In scope: any repository in this organization and the artifacts it
publishes. Repositories with product-specific threat surfaces (for
example, desktop IPC/capabilities, MCP transport, module loading, or the
build/release supply chain) document those specifics in their own
`CONTRIBUTING.md` or `SECURITY.md`.

Out of scope:

- Vulnerabilities in third-party services or LLM providers a product
  talks to — report those to the upstream vendor.
- Denial-of-service via local resource exhaustion in dev-only fixtures.
- Findings that require pre-existing physical access to a user's machine.
- Already-public issues in transitively pulled dependencies — these are
  resolved by upgrading on upstream disclosure.
