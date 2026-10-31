# MCPSTG-TRNS-05 --- Test HTTP Routing Header and JSON-RPC Consistency

`<a id="mcpstg-trns-05">`{=html}`</a>`{=html}

#### Summary

This test evaluates whether an MCP server and any HTTP reverse proxy,
API gateway, or middleware consistently interpret HTTP routing
information and the JSON-RPC message carried in the request body.
Inconsistencies can occur when different layers make security decisions
using different interpretations of the HTTP method, path, content type,
headers, or JSON-RPC method.

For example, a gateway may authorize or rate-limit a request based on
its HTTP route while the MCP server dispatches the JSON-RPC method from
the body. If the layers disagree about the effective operation, an
attacker may be able to bypass route-level controls, reach an unintended
handler, or cause inconsistent authentication, authorization, or
logging. The test must be adapted to the transport and endpoint actually
implemented by the server; it does not assume that every MCP deployment
uses HTTP.

#### Scenario

-   **MCP client:** `<TEST_CLIENT>` sending requests to
    `<MCP_HTTP_ENDPOINT>`.
-   **MCP server:** `<AUTHORIZED_LAB_SERVER>`.
-   **HTTP intermediary:** `<REVERSE_PROXY_OR_API_GATEWAY>` if present.
-   **Target operations:** `<ALLOWED_JSON_RPC_METHOD>` and
    `<RESTRICTED_JSON_RPC_METHOD>`.
-   **Trust boundary:** client ↔ HTTP intermediary ↔ MCP HTTP transport
    ↔ JSON-RPC dispatcher.
-   **Attacker position:** a client able to send HTTP requests to the
    exposed MCP endpoint.
-   **Potential impact:** bypass of route-level authentication or
    authorization, inconsistent rate limiting, request smuggling-like
    interpretation differences, incorrect handler dispatch, or audit-log
    evasion.

#### Test Objectives

-   Establish the expected HTTP method, path, content type, and required
    headers for the MCP endpoint.
-   Confirm the gateway and MCP server agree on which endpoint and
    JSON-RPC operation are being processed.
-   Verify that changing HTTP routing information does not cause a
    restricted JSON-RPC method to bypass controls.
-   Verify that unsupported HTTP methods, paths, and content types are
    rejected consistently.
-   Check that authentication, authorization, rate limits, and audit
    logging apply to the effective JSON-RPC operation.
-   Identify parser or normalization differences between the
    intermediary and MCP server.

#### Preconditions

-   Authorized lab environment and written scope.
-   An HTTP-based MCP endpoint and a documented transport configuration.
-   A valid baseline request for a harmless JSON-RPC operation.
-   At least one restricted or privileged operation that can be safely
    tested without changing production data.
-   Access to gateway and MCP server logs, where available.
-   Knowledge of the expected HTTP method, endpoint path, headers, and
    protocol version.

#### How to Test

##### 1. Manual Review

Review the transport and deployment design:

-   Identify the public HTTP route and the upstream route used by the
    MCP server.
-   Identify which HTTP methods are accepted.
-   Determine where authentication and authorization are enforced.
-   Determine whether gateway policy is based on path, HTTP method,
    headers, JSON-RPC method, or a combination.
-   Review path normalization, trailing-slash handling, URL decoding,
    and header forwarding.
-   Confirm the server validates the JSON-RPC envelope and dispatches
    only supported methods.

Do not assume that an HTTP method maps one-to-one to a JSON-RPC method.
Establish the intended mapping from the actual deployment.

##### 2. Configuration Review

Inspect:

-   Reverse-proxy and API-gateway route definitions.
-   HTTP method allow-lists and path rewrite rules.
-   Authentication, authorization, and rate-limit policies.
-   Content-type and request-body size restrictions.
-   Header allow-lists, forwarding behavior, and duplicate-header
    handling.
-   MCP server transport configuration and JSON-RPC dispatch logic.
-   Logging fields used to correlate the HTTP request with the
    dispatched JSON-RPC method.

Redact credentials and session tokens.

##### 3. Runtime Testing

1.  Send a valid, harmless request using the documented HTTP method,
    endpoint path, content type, and required headers. Record the HTTP
    status, response headers, JSON-RPC response, and server-side
    dispatch log.
2.  Repeat the request using an unsupported HTTP method while keeping
    the JSON-RPC body unchanged. Confirm it is rejected by the transport
    layer and is not dispatched unexpectedly.
3.  Send a request to an incorrect or unconfigured path with the same
    JSON-RPC body. Confirm it does not reach the MCP handler.
4.  Change the JSON-RPC `method` in the body to a restricted method
    while retaining the same permitted HTTP route. Verify that
    method-level authorization is still enforced.
5.  Where the deployment has route-specific policies, compare the
    gateway's decision with the MCP server's actual dispatch decision.
6.  Test missing, incorrect, or unsupported `Content-Type` values and
    malformed JSON bodies. Confirm the server rejects them safely and
    consistently.
7.  Test benign path-normalization variants relevant to the deployment,
    such as a trailing slash or documented URL-encoding cases. Do not
    use ambiguous or destructive payloads.
8.  Where duplicate or conflicting security-relevant headers are
    accepted by the HTTP stack, test them in the lab and confirm that
    the gateway and upstream do not interpret them differently.
9.  Compare gateway access logs with MCP server logs. Confirm both
    identify the same effective route and JSON-RPC method.
10. Repeat with authentication enabled and disabled only where the lab
    configuration explicitly permits it; verify that no alternate
    method/path combination bypasses authentication.

##### 4. Abuse Case Testing

Using only the authorized endpoint:

-   Attempt a restricted JSON-RPC method over an otherwise permitted
    HTTP route.
-   Attempt a permitted JSON-RPC method over an unsupported HTTP method
    or incorrect route.
-   Test path normalization differences that are plausible for the
    actual proxy/server stack.
-   Test conflicting or duplicated headers only if the intermediary
    accepts them and the test is explicitly in scope.
-   Check whether rate limiting and audit logging are applied to the
    actual JSON-RPC operation rather than only to the outer HTTP route.

Do not perform high-volume request smuggling or denial-of-service
testing unless separately authorized.

##### 5. Log and Detection Review

Confirm logs record enough information to correlate:

-   HTTP method and normalized route.
-   Authenticated principal or client identity.
-   JSON-RPC method, when safely parsed.
-   Gateway decision and upstream dispatch result.
-   Rejection reason and correlation/request identifier.

Check for discrepancies where the gateway records one route or method
but the MCP server dispatches another operation.

#### Example Snippets

Illustrative baseline HTTP request. Replace the path, headers, and
JSON-RPC method with those documented by the target deployment.

``` http
POST /<MCP_ENDPOINT> HTTP/1.1
Host: <LAB_HOST>
Content-Type: application/json
Authorization: Bearer <LAB_TOKEN>

{
  "jsonrpc": "2.0",
  "id": 31,
  "method": "<HARMLESS_JSON_RPC_METHOD>",
  "params": {}
}
```

Illustrative method-mismatch test: keep the documented HTTP route but
change the JSON-RPC method to a restricted operation.

``` json
{
  "jsonrpc": "2.0",
  "id": 32,
  "method": "<RESTRICTED_JSON_RPC_METHOD>",
  "params": {}
}
```

These snippets are test patterns, not universal transport requirements.
Use the target server's documented HTTP transport contract.

#### Expected Results

**Secure result:**

-   Only documented HTTP methods, paths, content types, and transport
    headers are accepted.
-   Unsupported HTTP requests are rejected before unintended JSON-RPC
    dispatch.
-   JSON-RPC method-level authorization is enforced independently of the
    outer HTTP route.
-   Gateway and MCP server interpret the effective request consistently.
-   Path and header normalization cannot be used to bypass security
    controls.
-   Rate limits and audit logs apply to the effective operation.
-   Malformed or ambiguous requests fail safely without reaching an
    unintended handler.

**Potential finding indicators:**

-   A restricted JSON-RPC method is dispatched through a route that the
    gateway considers permitted.
-   Changing the HTTP method or path bypasses authentication,
    authorization, or rate limiting.
-   The gateway and MCP server interpret a path or security-relevant
    header differently.
-   Unsupported content types or malformed bodies reach a handler that
    should reject them.
-   Audit logs identify a harmless route or operation while the server
    executes a different JSON-RPC method.
-   An alternate path or method exposes a handler that is not intended
    to be publicly reachable.

#### Remediation

-   Define and enforce a single documented HTTP transport contract for
    each MCP endpoint.
-   Apply authentication and authorization at the MCP method/operation
    level, not solely at the outer HTTP route.
-   Keep gateway and upstream route definitions and normalization
    behavior consistent.
-   Reject unsupported HTTP methods, paths, content types, malformed
    JSON, and ambiguous security-relevant headers.
-   Normalize paths once at a trusted boundary and ensure all downstream
    components use the same canonical value.
-   Avoid relying on client-supplied headers to determine identity or
    authorization.
-   Apply rate limits to the effective operation and authenticated
    principal.
-   Correlate gateway and server logs using a request identifier and
    record the actual dispatched JSON-RPC method.
-   Keep transport-specific controls separate from JSON-RPC method
    authorization so one layer cannot silently substitute for the other.

#### Evidence to Collect

-   Baseline and negative HTTP requests.
-   HTTP responses and relevant response headers.
-   Gateway route/policy configuration with secrets redacted.
-   Gateway and MCP server logs for the same request identifiers.
-   Evidence of the actual JSON-RPC method dispatched.
-   Reproduction steps and the demonstrated security-control bypass, if
    any.

#### Suggested Mappings

-   **CWE:** CWE-436 --- Interpretation Conflict; CWE-444 ---
    Inconsistent Interpretation of HTTP Requests (HTTP Request/Response
    Smuggling) only where the behavior meets that definition; CWE-863
    --- Incorrect Authorization; CWE-693 --- Protection Mechanism
    Failure.
-   **OWASP:** OWASP API Security Top 10 API5:2023 --- Broken Function
    Level Authorization, where a restricted operation is exposed;
    relevant HTTP request-smuggling guidance only when a genuine parser
    discrepancy is demonstrated.
-   **Severity:** Context-dependent. Base severity on the operation
    reached and the control bypass demonstrated. Do not label a harmless
    transport inconsistency High without an exploitable impact.
-   **Test type:** Dynamic / Hybrid.

#### References

-   MCP specification and transport documentation applicable to the
    protocol version under test.
-   HTTP server, reverse-proxy, and API-gateway documentation for the
    deployed stack.
