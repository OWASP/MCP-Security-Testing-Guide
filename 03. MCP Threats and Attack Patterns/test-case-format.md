# Test case format

Authoring template for the test cases in [sections 3.01–3.19](<3. MCP Threats and Attack Patterns.md>). Read this before adding or editing a test.

Every test in this chapter is written to the same shape so that a reader can run it and a reviewer can check it. The 79 tests in `3.01`–`3.19` are the reference implementation of the template below.

## Where tests live

- One file per category: `3.01-…` through `3.19-…`.
- Each file starts with category context (overview, scope, related categories, common test chains), then published threat write-ups, then `## Test cases`.
- `## Test cases` contains the summary table, followed by one `### MCPSTG-…` block per test.

## Test identifiers

- Format: `MCPSTG-<PREFIX>-<NN>` — for example `MCPSTG-INFO-01`.
- `<PREFIX>` is the category prefix (table below); `<NN>` is zero-padded and restart-per-category.
- Every test block carries an explicit HTML anchor immediately after its heading so the summary table can link to it:

```markdown
### MCPSTG-INFO-01 — Identify MCP Servers and Clients

<a id="mcpstg-info-01"></a>
```

### Category prefixes

| Section | Category | Prefix |
| --- | --- | --- |
| 3.01 | Information Gathering | `INFO` |
| 3.02 | Configuration and Deployment | `CONF` |
| 3.03 | Identity and Authentication | `AUTHN` |
| 3.04 | Authorization and Permission | `AUTHZ` |
| 3.05 | Tool Security | `TOOL` |
| 3.06 | Resource and Data Access | `RSRC` |
| 3.07 | Prompt and Instruction | `PRMT` |
| 3.08 | Context and Memory | `CTX` |
| 3.09 | Agentic Workflow | `AGNT` |
| 3.10 | Input Validation | `INPV` |
| 3.11 | Output Handling | `OUTV` |
| 3.12 | Logging and Detection | `LOG` |
| 3.13 | Supply Chain | `SUPP` |
| 3.14 | Enterprise Governance | `GOV` |
| 3.15 | Transport and Channel | `TRNS` |
| 3.16 | Gateway and Egress | `GW` |
| 3.17 | Secrets and Credentials | `SECR` |
| 3.18 | Resilience and Abuse | `ABUS` |
| 3.19 | Privacy and Retention | `PRVC` |

## Summary table

Each section carries one table under `## Test cases`. Keep it in sync with the test blocks — the `View` link must resolve to that test's anchor.

| Section | Test ID | Name | Severity | Type | View |
| --- | --- | --- | --- | --- | --- |
| 3.01 | `MCPSTG-INFO-01` | Identify MCP Servers and Clients | Medium | Hybrid | [View](#mcpstg-info-01) |

- **Severity** uses the bands applied across the chapter: `Critical`, `High`, `Medium`, `Low`.
- **Type** is `Manual`, `Hybrid`, or `Automated`.

## Test block template

```markdown
### MCPSTG-XXX-NN — Short imperative title

<a id="mcpstg-xxx-nn"></a>

#### Summary

One paragraph: what is being tested and why it matters.

#### Scenario

The abuse case in concrete terms: who the attacker is, what they control, and what the test exercises.

#### Preconditions

- Authorized lab environment and written scope.
- Access to host configuration, MCP server configuration, and (if applicable) gateway policy.
- Test principal `<TEST_USER>`; secondary account if testing cross-user issues.
- Log access for host, gateway, and MCP server.

#### Test Objectives

What a pass and a fail prove, stated as observations rather than opinions.

#### Tools

The tool categories needed (see [Appendix F — Testing Tools](../11. Appendix F - Testing Tools.md)). Describe capability, not products.

#### Test Data / Example Payloads

Synthetic, lab-safe inputs only, built from the [placeholders](../10. Appendix D - Safe Lab Fixtures.md).

#### How to Test

1. Connect the lab host to `<AUTHORIZED_LAB_SERVER>`.
2. Capture a baseline.
3. Execute the bounded runtime checks with synthetic arguments only.
4. Record host, server and gateway responses plus redacted logs.

#### Expected Results

- **Secure:** the control blocks or contains the abuse, with a stable deny/alert reason.
- **Insecure:** the abuse succeeds as described and the sensitive effect occurs without detection.
- **Evidence:** redacted logs, config excerpts, request/response pairs, policy screenshots.

#### Example snippets

Only where a snippet adds something the prose cannot — JSON-RPC, host config, or a lab script. Mark every placeholder.

#### Mapping

- OWASP MCP Top 10 / OWASP LLM Top 10 item, CWE, MITRE ATLAS technique, and any ASVS chapter.

#### Remediation

The specific change that makes the test pass, addressed to a developer or administrator.

#### References

Sourced, versioned links — the specification, the advisory, the disclosure.
```

## Writing rules

- **Vendor-neutral.** Describe control patterns and tool categories, never product marketing.
- **Lab-only.** Use placeholders from [Appendix D — Safe Lab Fixtures](../10. Appendix D - Safe Lab Fixtures.md). Never document steps that target real organizations, customers or non-lab endpoints.
- **Sourced claims.** Version ranges, dates and quotes come from the linked source; state them as the source does, and say when they were checked.
- **One test, one observation.** If the pass condition needs two unrelated observations, it is two tests.
- **Keep the summary table, anchors, and blocks consistent** — see [Taxonomy and identifiers](taxonomy.md).

## Red team checklist

<a id="mcp-red-team-checklist"></a>

Rules of engagement for anyone using the tests in this chapter offensively:

- [ ] **Written authorization** for every target, signed and dated, naming the systems and the window.
- [ ] **Scope** agreed in writing — hosts, MCP servers, tools, data classes — and out-of-scope systems identified explicitly.
- [ ] **Lab environment** identified; production only where the engagement explicitly covers it.
- [ ] **Synthetic data** for payloads; no personal data, customer records or live credentials.
- [ ] **Placeholders** used consistently (`<TEST_USER>`, `<TEST_WORKSPACE>`, `<AUTHORIZED_LAB_SERVER>`, `<TEST_TOOL_NAME>`, `<TEST_RESOURCE>`); no real hostnames or account names in write-ups.
- [ ] **Blast radius** understood before running destructive, write, install, network-egress or approval-bypass tests.
- [ ] **No persistence** — servers, tokens, cron entries, or rules you added must be removed when the test ends.
- [ ] **Evidence handling** agreed up front; secrets encountered are redacted and reported, never copied.
- [ ] **Stop conditions** agreed — the trigger that ends the test, and who calls it.
- [ ] **Detection and response teams informed** where the engagement covers them, so a real alert is not mistaken for the test.
- [ ] **Findings reported** through the [finding template](#mcp-red-team-finding-template), with reproduction steps that a defender can replay in a lab.

## Red team finding template

<a id="mcp-red-team-finding-template"></a>

Use this shape for each finding, so results line up with the taxonomy and the review process:

| Field | What to record |
| --- | --- |
| Title | Short, specific, and testable |
| Test ID | The `MCPSTG-…` test that exposed it |
| Affected component | MCP host, client, server, tool, prompt, resource, transport, registry, dependency, or workflow |
| Attack path | Step-by-step explanation of how abuse happens |
| Impact | What the attacker can read, change, execute, delete, or exfiltrate |
| Framework mapping | OWASP MCP, OWASP LLM, CWE, MITRE ATLAS, STRIDE/DREAD/MAESTRO |
| Evidence | PoC, logs, screenshots, tool output, advisory, CVE, paper, or lab reference |
| Fix guidance | Practical mitigations and secure design alternatives |
| Detection guidance | Logs, events, alerts, and telemetry to monitor |
| Severity | Critical / High / Medium / Low, with the reasoning stated |

See [Appendix C — Security Review](../09. Appendix C - Security Review.md) for the review status values, scorecard, and the security review template.
