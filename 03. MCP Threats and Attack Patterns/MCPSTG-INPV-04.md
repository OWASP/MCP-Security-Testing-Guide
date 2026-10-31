# MCPSTG-INPV-04 --- Test Input Validation Across Multi-Round Interactions

`<a id="mcpstg-inpv-04">`{=html}`</a>`{=html}

#### Summary

This test evaluates whether an MCP server validates input consistently
across every round of a multi-step interaction, rather than validating
only the initial request. Multi-round workflows may include an initial
user-supplied value, a server response, a follow-up request, and
additional arguments or context supplied before the operation completes.
If later-round values bypass the same schema, type, length, encoding,
authorization-context, or semantic checks applied to the first round, an
attacker may be able to introduce malformed or unexpected data after the
initial validation boundary.

The test focuses on **validation consistency across interaction
rounds**. It does not assume that every MCP interaction is multi-round;
perform it only for methods or workflows in scope that accept follow-up
input or continue an operation over multiple messages.

#### Scenario

-   **MCP host/client:** `<TEST_CLIENT>` using `<TEST_ACCOUNT>`.
-   **MCP server:** `<AUTHORIZED_LAB_SERVER>` exposing
    `<TARGET_TOOL_OR_WORKFLOW>`.
-   **Workflow:** `<MULTI_ROUND_WORKFLOW>` with at least two input or
    continuation stages.
-   **Trust boundary:** client/host ↔ MCP server ↔ downstream
    application or service.
-   **Attacker position:** an authenticated or unauthenticated client,
    as defined by the test scope, able to influence one or more rounds
    of input.
-   **Potential impact:** validation bypass, unexpected downstream
    operations, injection into a backend component, resource exhaustion,
    or inconsistent policy enforcement.

#### Test Objectives

-   Identify every round in which client-controlled or externally
    influenced data enters the workflow.
-   Verify that each round is checked against the expected schema and
    semantic constraints.
-   Confirm that validation is performed server-side and is not
    delegated solely to the host or client.
-   Check that values cannot change type, meaning, scope, or
    authorization context between rounds without revalidation.
-   Verify that malformed or out-of-policy follow-up input is rejected
    safely and does not partially execute a sensitive operation.

#### Preconditions

-   Authorized lab environment and written scope.
-   A target MCP server and a documented multi-round workflow.
-   A valid baseline input that completes the workflow successfully.
-   Test fixtures for boundary values, invalid types, oversized values,
    malformed encodings, and semantically invalid values.
-   Access to relevant server-side and downstream logs where available.
-   A non-production account and synthetic data; do not use real
    customer records or destructive operations.

#### How to Test

##### 1. Manual Review

Review the workflow implementation and documentation to identify:

-   The initial request and every subsequent request or continuation
    message.
-   Which fields are client-controlled, server-generated, or derived
    from prior responses.
-   The schema and business rules expected at each stage.
-   Whether validation is repeated after a continuation, state
    transition, or change of principal/session.
-   Whether downstream calls receive the validated value or a separately
    reconstructed value.

Record the expected type, format, maximum length, allowed values, and
authorization requirements for each input field.

##### 2. Configuration Review

Inspect:

-   Tool and workflow input schemas.
-   Server-side validation libraries and custom validators.
-   Limits for string length, array size, nesting depth, numeric ranges,
    and request size.
-   Any host, gateway, or middleware validation that might be
    incorrectly treated as the only validation layer.
-   Error handling and logging for rejected continuation input.

Do not expose secrets or production values in evidence.

##### 3. Runtime Testing

1.  Start a clean session and submit a valid first-round input. Record
    the response and the expected next step.
2.  Continue the workflow with valid follow-up input. Confirm that the
    baseline completes as designed.
3.  Repeat the workflow, changing one follow-up field at a time to an
    invalid type (for example, string instead of integer), missing
    required field, unexpected field, or invalid enum value.
4.  Test boundary values at and just beyond documented limits, such as
    maximum string length, array count, numeric range, and nesting
    depth.
5.  Test malformed encodings and control characters only where those
    input formats are accepted by the workflow.
6.  Where a later round accepts an identifier, path, URL, object
    reference, or resource name, substitute a synthetic value outside
    the permitted scope and verify that it is revalidated.
7.  If the workflow carries state between rounds, alter a
    client-controlled value from an earlier response or continuation
    request and verify that the server does not trust it without
    checking its integrity and association with the current session.
8.  Confirm rejected input does not trigger the downstream action,
    create a partial object, or leave the workflow in an inconsistent
    state.
9.  Repeat using a fresh session to distinguish a deterministic
    validation result from state left by a prior test.

##### 4. Abuse Case Testing

Using only synthetic lab data:

-   Submit a valid first round followed by an invalid second or later
    round.
-   Replay a continuation with altered fields or an expired/invalid
    workflow reference.
-   Attempt to exceed documented size or count limits across multiple
    rounds, not only within one request.
-   Change values that affect the target, tenant, user, or resource
    between rounds and check whether the server reauthorizes the final
    operation.
-   Check whether repeated invalid continuations cause disproportionate
    CPU, memory, backend requests, or persistent state.

Avoid destructive payloads and stop if the test affects shared services.

##### 5. Log and Detection Review

Confirm logs can correlate the interaction rounds using a non-sensitive
session or request identifier and record:

-   Which stage rejected the input.
-   The validation rule or category that failed.
-   Whether a downstream operation was attempted.
-   Whether the workflow was safely terminated or returned to a valid
    state.

Logs should not store secrets, tokens, or unnecessary sensitive input
values.

#### Example Snippets

Illustrative follow-up request. Adapt the method and fields to the
actual workflow; this is not a universal MCP request schema.

``` json
{
  "jsonrpc": "2.0",
  "id": 12,
  "method": "<WORKFLOW_CONTINUATION_METHOD>",
  "params": {
    "workflowId": "<LAB_WORKFLOW_ID>",
    "input": {
      "recordCount": "not-an-integer"
    }
  }
}
```

Example invalid test values:

``` json
{
  "recordCount": "not-an-integer",
  "displayName": "<VALUE_EXCEEDING_DOCUMENTED_LIMIT>",
  "resourceId": "<SYNTHETIC_OUT_OF_SCOPE_RESOURCE>",
  "mode": "<UNSUPPORTED_ENUM_VALUE>"
}
```

#### Expected Results

**Secure result:**

-   Each round is validated server-side against the applicable schema
    and business rules.
-   Invalid or out-of-policy follow-up input is rejected before
    sensitive downstream processing.
-   State, session, tenant, and authorization context are bound to the
    correct interaction and rechecked when relevant.
-   Rejection does not leave partial or inconsistent state.
-   Error responses provide enough information for legitimate debugging
    without exposing internal data or secrets.

**Potential finding indicators:**

-   The first round is validated but a later round accepts malformed or
    out-of-policy input.
-   A follow-up value changes the target, tenant, user, or resource
    without fresh authorization.
-   A rejected round still triggers a downstream operation or creates
    persistent partial state.
-   Multi-round input bypasses documented size, type, or semantic
    constraints.
-   Repeated invalid continuation requests cause resource exhaustion
    beyond the documented limits.

#### Remediation

-   Apply server-side schema and semantic validation at every input
    boundary, including continuation and follow-up stages.
-   Validate the final value actually passed to the downstream
    component; do not rely only on client-side or initial-request
    validation.
-   Enforce consistent type, length, range, allow-list, and nesting
    constraints.
-   Bind workflow state to the authenticated principal, session, and
    tenant; protect state against tampering and replay.
-   Reauthorize sensitive actions when the target resource or effective
    identity can change between rounds.
-   Fail closed on invalid continuation input and avoid partial side
    effects.
-   Apply request-size, rate, and workflow-lifetime limits.
-   Log validation outcomes with correlation identifiers while
    minimizing sensitive data.

#### Evidence to Collect

-   Sanitized initial and follow-up requests.
-   Responses for valid and invalid test cases.
-   Relevant input schema and validation configuration.
-   Correlated server logs showing the rejected stage and downstream
    execution status.
-   Reproduction steps and the observed security impact.

#### Suggested Mappings

-   **CWE:** CWE-20 --- Improper Input Validation; CWE-1284 --- Improper
    Validation of Specified Quantity in Input (where applicable);
    CWE-116 --- Improper Encoding or Escaping of Output (only if the
    observed issue is output encoding).
-   **OWASP:** OWASP Top 10 2025 A05 --- Injection, where an exploitable
    injection path is demonstrated; otherwise map to the relevant
    input-validation/control category used by the project.
-   **Severity:** Context-dependent. Do not assign High solely because
    validation differs; base severity on demonstrated downstream impact.
-   **Test type:** Dynamic / Hybrid.

#### References

-   MCP specification and SDK documentation applicable to the protocol
    version under test.
-   The target server's published tool/workflow schemas and input
    constraints.
