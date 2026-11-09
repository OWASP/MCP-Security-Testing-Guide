# Test ID taxonomy

How test identifiers are built, and what each prefix covers.

## Format

`MCPSTG-<PREFIX>-<NN>`

- `MCPSTG` — this guide.
- `<PREFIX>` — the category (table below).
- `<NN>` — a two-digit, per-category sequence, starting at `01`.

Identifiers are referenced in prose as backticked codes (`MCPSTG-INFO-01`) and are stable: a test that is withdrawn leaves a gap rather than renumbering the ones after it.

## Prefix matrix

| Section | Category | Prefix | What the tests in the category establish |
| --- | --- | --- | --- |
| 3.01 | Information Gathering | `INFO` | The attack surface: hosts, clients, servers, tools, resources, transports, trust boundaries and context flows. |
| 3.02 | Configuration and Deployment | `CONF` | Whether the deployment is safely configured: server definitions, local exposure, debug output, file permissions, transports. |
| 3.03 | Identity and Authentication | `AUTHN` | Whether callers and servers authenticate, and whether tokens are handled, scoped, expired and revoked correctly. |
| 3.04 | Authorization and Permission | `AUTHZ` | Whether permissions are least-privilege and enforced per action, per user and per workspace, including approvals and chaining. |
| 3.05 | Tool Security | `TOOL` | Whether tools can be poisoned, invoked unsafely, chained dangerously, or approved without informed consent. |
| 3.06 | Resource and Data Access | `RSRC` | Whether resources leak, enumerate, cross workspace or tenant boundaries, or expose secrets and files. |
| 3.07 | Prompt and Instruction | `PRMT` | Whether instructions can be injected, overridden, hidden or leaked through prompts and tool output. |
| 3.08 | Context and Memory | `CTX` | Whether context over-shares, persists, leaks, crosses sessions, or lets untrusted content outrank trusted content. |
| 3.09 | Agentic Workflow | `AGNT` | Whether autonomy, multi-step workflows, goal handling and retry behaviour stay within intended limits. |
| 3.10 | Input Validation | `INPV` | Whether tool inputs are validated: parameters, paths, and JSON/schema confusion. |
| 3.11 | Output Handling | `OUTV` | Whether tool output is rendered and filtered safely, and whether sensitive data appears in results. |
| 3.12 | Logging and Detection | `LOG` | Whether tool calls, approvals, injection attempts and secret exposure are logged, detectable and reconstructable. |
| 3.13 | Supply Chain | `SUPP` | Whether server provenance, dependencies, installation, registry trust and updates are verifiable. |
| 3.14 | Enterprise Governance | `GOV` | Whether inventory, approved registries, policy, exceptions and compliance evidence exist and are enforced. |
| 3.15 | Transport and Channel | `TRNS` | Whether TLS, transport authentication binding, sizing and timeouts are correct, and whether stdio servers start with only the environment they were granted. |
| 3.16 | Gateway and Egress | `GW` | Whether gateway allowlists, SSRF protections and rate limiting hold. |
| 3.17 | Secrets and Credentials | `SECR` | Whether secrets avoid configuration and environment exposure, are stored and rotated properly, and are redacted. |
| 3.18 | Resilience and Abuse | `ABUS` | Whether tool-call storms, concurrency and retry behaviour stay bounded and safe. |
| 3.19 | Privacy and Retention | `PRVC` | Whether PII, retention and downstream copying are minimized and labelled. |

## Reading the matrix

- **Prefixes are categories, not severities.** A `LOG` test can be `Critical` (an unaudited approval) and an `INFO` test is usually `Medium`.
- **Cross-category chains are normal.** A finding often needs tests from two or three prefixes; each category file lists the chains it participates in under `Common test chains`.
- **Related identifiers, not related sections.** Cite tests by identifier so the reference survives file changes.

Authoring rules, the summary table format and the test block template are in [Test case format](test-case-format.md).
