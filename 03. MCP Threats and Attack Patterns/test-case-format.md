# Test Case Format and Lab Guidance

[← Chapter 3 overview](<3. MCP Threats and Attack Patterns.md>) · [Contributing](../CONTRIBUTING.md)

Tests live in the Chapter 3 category pages (`3.01`–`3.19`), under **Test cases**. This page provides authoring conventions and synthetic lab prerequisites; it is not a runnable MCP server or test suite.

## Test case format

Use the following structure for a test block in its category page. Keep its ID stable and update the category's summary table when its title, risk, or testing type changes.

```markdown
### MCPSTG-CATEGORY-NN — <Test Name>

<a id="mcpstg-category-nn"></a>

#### Summary
Describe the observable problem and affected component.

#### Scenario
Identify the client, server, transport, trust boundary, and lab fixtures.

#### Test Objectives
State the control being checked.

#### Preconditions
Specify authorization, configuration, access, and required observables.

#### How to Test
##### 1. Manual Review
##### 2. Configuration Review
##### 3. Runtime Testing
##### 4. Abuse Case Testing
##### 5. Log and Detection Review

#### Example snippets
Include bounded examples where they help reproduce the test.

#### Test Data / Example Payloads
Use synthetic values and define any additional fixtures.

#### Expected Results
Distinguish secure and insecure behavior using observable outcomes.

#### Remediation
Describe controls that address the demonstrated failure.

#### Tools
Identify applicable tool categories and their prerequisites.

#### References
Cite sources and the protocol revision in scope.

#### Mapping
Include related standards requirements only where applicable, with versioned sources.
Risk level: Low / Medium / High / Critical
Testing type: Manual / Automated / Hybrid
```

## Safe lab fixtures

<a id="safe-lab-fixtures"></a>

Use synthetic values only. These conventions describe fixtures that the tester must provide; substituting placeholders does not create a working lab.

| Placeholder | Meaning |
| --- | --- |
| `<TEST_USER>` | An authorized lab principal; use a second synthetic principal when the test requires isolation checks. |
| `<TEST_WORKSPACE>` | A dedicated sandbox directory containing only test data. |
| `<TEST_TOOL_NAME>` | A synthetic tool identifier matching the lab server's advertised schema. |
| `<TEST_RESOURCE>` | A synthetic resource URI advertised by the lab server. |
| `<AUTHORIZED_LAB_SERVER>` | An explicitly in-scope lab server; use a lab-owned address when the example needs a network destination. |

Suggested fixtures:

- An echo tool that returns synthetic arguments unchanged.
- A read-only query tool backed by a fixed, in-memory dataset.
- A write tool restricted to `<TEST_WORKSPACE>/sandbox/`.
- A benign document resource and a separate document containing obvious, harmless test instructions.

```text
<TEST_WORKSPACE>/
  sandbox/     # approved write targets
  readonly/    # synthetic read-only documents
  secrets/     # fake-secret negative-test fixtures; denied to tested tools
```

Populate `secrets/` with canaries such as `FAKE_API_KEY=MCPSTG_LAB_ONLY_NOT_A_CREDENTIAL`. Do not use customer data or real credentials. Match each tool's name, arguments, and resource URI to the actual lab implementation. Define any test-specific behavior, such as token issuance, tenant isolation, or an observable side-effect counter, in that test's preconditions.

Outbound requests must remain within the authorized lab. Use controlled destinations that record requests safely without forwarding them to third-party services.

## Testing tools

<a id="testing-tools"></a>

Choose tools appropriate to the transport and control under review. Review any packages or servers before installing or executing them; the guide does not supply or endorse an executable harness.

| Task | Tool category |
| --- | --- |
| HTTP, OAuth, and gateway inspection | HTTP proxy and request/response inspection tools |
| TLS configuration and certificates | TLS analyzers and certificate inspection tools |
| MCP requests and argument validation | JSON/JSON-RPC inspection tools and a compatible MCP client |
| Local processes and workspace boundaries | Process monitors, filesystem permission tools, and source review |
| Logs, traces, and detection | Redacted log search, trace inspection, and detection-rule dry runs |
| Dependencies and provenance | Dependency scanners, signature verification, and provenance inspection |

Record tool versions and configuration. Run active checks only within written scope and the lab's load limits.

## Running a test

<a id="running-a-test"></a>

1. Confirm the authorized systems, transports, principals, and stopping conditions.
2. Prepare the required synthetic fixtures and host/server/gateway observables.
3. Start with [Information Gathering](3.01-information-gathering.md) and select applicable tests from the [category table](<3. MCP Threats and Attack Patterns.md#test-categories--sections-31-to-319>).
4. Record the client/server versions and MCP protocol revision. Follow the selected test's preconditions and steps. If a prerequisite or deciding observable is unavailable, record **not tested** with the reason; do not infer a pass.
5. Capture the input, response, policy decision, and relevant protected-action or data-flow evidence. Compare the observations with that test's expected results.
6. Remove synthetic artifacts, invalidate lab credentials where applicable, and restore the lab configuration. Keep redacted evidence and record any cleanup that could not be completed.

Use the finding template below for a demonstrated defect. [Appendix C](<../09. Appendix C - Security Review.md#how-to-record-a-review>) defines the status values and evidence fields for the broader security review.

## MCP red team checklist

<a id="mcp-red-team-checklist"></a>

- Obtain written authorization naming systems, testers, dates, and permitted actions.
- Use synthetic data and canaries; simulate exfiltration and side effects inside the lab.
- Define request, concurrency, and cost limits before runtime checks.
- Identify who can stop the exercise and how to disable the tested integration.
- Collect redacted evidence without copying real secrets. Link observations to the relevant test ID.

Use the existing category procedures for the control-specific checks rather than treating this checklist as a separate test catalog.

## MCP red team finding template

<a id="mcp-red-team-finding-template"></a>

```markdown
# MCP Red Team Finding

## Title and Severity

## Test ID and Affected Components
Client/host, server, tool/resource, transport, protocol revision, and versions:

## Preconditions and Reproduction
Authorized lab scope, configuration, synthetic inputs, and exact steps:

## Expected and Observed Behavior
Include the deciding observable and any validation limitations:

## Evidence
Redacted requests/responses, policy decisions, logs, and side-effect or data-flow observations:

## Impact and Root Cause
Separate demonstrated effects from assumptions:

## Recommended Remediation

## Owner and Follow-up
```
