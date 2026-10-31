# MCPSTG-AUTHZ-06 --- Test Subscription Authorization and Notification Isolation

`<a id="mcpstg-authz-06">`{=html}`</a>`{=html}

#### Summary

This test evaluates whether an MCP server enforces resource-level
authorization when a client subscribes to resource updates and
throughout the lifetime of that subscription. It checks both
**authorization at subscription time** and **authorization when
notifications are delivered**. A server may correctly restrict
`resources/read` while still allowing an unauthorized principal to
establish a subscription or receive update notifications for a protected
resource.

The test also checks whether subscription state is isolated between
principals and whether access revocation is applied to
already-established subscriptions. A subscription identifier is a
correlation value; possession or knowledge of that identifier must not
be treated as proof of authorization.

This test is distinct from `MCPSTG-RSRC-06`: RSRC-06 focuses on
resource/path existence disclosure through subscription errors, while
this test focuses on unauthorized subscription access and notification
delivery.

#### Scenario

-   **MCP host/client:** two separate test clients or sessions
    representing `<USER_ALICE>` and `<USER_BOB>`.
-   **MCP server:** `<AUTHORIZED_LAB_SERVER>` exposing resource
    subscriptions.
-   **Protected resources:** `<ALICE_PRIVATE_RESOURCE>` and
    `<BOB_PRIVATE_RESOURCE>`.
-   **Access policy:** Alice is authorized for Alice's resource but not
    Bob's; Bob has the inverse permissions.
-   **Trust boundary:** authenticated client/session ↔ MCP server
    subscription manager ↔ resource provider/event source.
-   **Attacker position:** an authenticated lower-privileged user
    attempting to subscribe to another user's resource or receive
    notifications outside their authorization scope.
-   **Potential impact:** disclosure of sensitive resource identifiers,
    update metadata, or resource contents; cross-user or cross-tenant
    information leakage.

#### Test Objectives

-   Confirm the server authorizes each requested resource subscription
    against the requesting principal.
-   Confirm unauthorized resource subscriptions are rejected or excluded
    from the accepted subscription set.
-   Confirm update notifications are delivered only to principals
    currently authorized to receive them.
-   Confirm revoking access terminates or suppresses notifications for
    existing subscriptions.
-   Confirm subscription state and notification routing are isolated
    across users, sessions, and tenants.
-   Confirm notification filters do not result in delivery of
    unrequested or unauthorized event data.

#### Preconditions

-   Authorized lab environment and written scope.
-   Two distinct authenticated principals with deliberately different
    resource permissions.
-   At least one synthetic private resource for each principal.
-   A resource provider capable of generating a harmless update
    notification.
-   A way to observe each client's response stream independently.
-   Administrative access to modify the test ACL or revoke a test user's
    resource permission.
-   Server and gateway logs, where available.

#### How to Test

##### 1. Manual Review

Review the subscription implementation and authorization design:

-   Identify where the authenticated principal is obtained for a
    subscription request.
-   Determine whether the subscription handler checks access to the
    specific resource URI.
-   Determine whether authorization is checked only when the
    subscription is created or also when notifications are emitted.
-   Review how subscriptions are indexed and associated with users,
    sessions, tenants, and resource identifiers.
-   Check whether a subscription identifier is ever used as a substitute
    for an authorization check.
-   Review how permission changes, logout, session expiry, and
    disconnect affect active subscriptions.

##### 2. Configuration Review

Inspect:

-   Resource-level ACLs and tenant boundaries.
-   Authentication middleware and the identity/context passed to
    subscription handlers.
-   Subscription storage and event-routing configuration.
-   Notification filters and any server-side event fan-out logic.
-   Session expiry, revocation, and cleanup settings.

Redact tokens, credentials, and personal data from evidence.

##### 3. Runtime Testing

1.  Authenticate as Alice and confirm Alice can access
    `<ALICE_PRIVATE_RESOURCE>` but cannot access
    `<BOB_PRIVATE_RESOURCE>` using the server's normal authorization
    mechanism.
2.  As Alice, open a subscription requesting updates for
    `<ALICE_PRIVATE_RESOURCE>`. Record the acknowledgement and the
    accepted notification filters.
3.  As Alice, attempt to subscribe to `<BOB_PRIVATE_RESOURCE>`. Record
    whether the server rejects the request or excludes the unauthorized
    resource from the accepted subscription.
4.  Authenticate as Bob in a separate client/session and subscribe to
    `<BOB_PRIVATE_RESOURCE>`.
5.  Trigger a harmless update to Bob's resource. Confirm Bob receives
    the expected notification and Alice does not.
6.  Trigger a harmless update to Alice's resource. Confirm Alice
    receives the expected notification and Bob does not.
7.  While Alice has a valid subscription to her own resource, revoke
    Alice's access to that resource using the lab ACL. Trigger another
    update and observe whether Alice still receives notifications.
8.  Repeat the revocation test with session expiry or logout if those
    lifecycle events are in scope.
9.  Where multiple tenants are supported, repeat with two synthetic
    tenants and resources that have similar names or identifiers to
    detect routing mistakes.
10. Record the subscription acknowledgement, notification stream,
    principal/session identity, ACL state, and server-side routing
    decision for each test.

##### 4. Abuse Case Testing

Using only the two lab principals and synthetic resources:

-   Attempt to subscribe to another user's resource by changing only the
    resource URI.
-   Attempt to use a subscription identifier observed in one test
    session from the other session. Do not assume the identifier is a
    credential; verify whether it can influence routing or access.
-   Keep a subscription open while access is revoked, then generate a
    new update.
-   Reconnect after logout or session expiry and check whether stale
    subscription state is reused.
-   If notification filters are supported, request a narrow filter and
    verify the server does not send unrelated event types or resources.
-   Check whether notifications expose sensitive URI names, metadata, or
    content even when the client cannot call `resources/read`.

##### 5. Log and Detection Review

Confirm logs can show:

-   The authenticated principal and tenant associated with subscription
    creation.
-   The resource authorization decision.
-   Subscription creation, rejection, revocation, and cleanup.
-   Notification routing decisions and delivery failures.
-   Whether a notification was suppressed after an ACL or session
    change.

Avoid logging access tokens or full sensitive resource contents.

#### Example Snippets

Illustrative subscription request. Adapt the notification envelope and
metadata to the protocol version and server implementation under test.

``` json
{
  "jsonrpc": "2.0",
  "id": 21,
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "resourceSubscriptions": [
        "<BOB_PRIVATE_RESOURCE>"
      ]
    }
  }
}
```

Example two-principal test matrix:

  Principal   Resource                 Expected authorization
  ----------- ------------------------ ------------------------
  Alice       Alice private resource   Allow
  Alice       Bob private resource     Deny
  Bob         Bob private resource     Allow
  Bob         Alice private resource   Deny

#### Expected Results

**Secure result:**

-   The server evaluates resource authorization using the identity of
    the requesting principal.
-   An unauthorized subscription is rejected or not included in the
    accepted subscription set.
-   Notifications are routed only to currently authorized subscribers.
-   Revocation, logout, and session expiry are reflected in active
    subscription behavior according to the server's documented policy.
-   Subscription identifiers correlate notifications with the correct
    request but do not grant access by themselves.
-   A client receives only the notification types and resource updates
    it is authorized and configured to receive.

**Potential finding indicators:**

-   Alice can establish an effective subscription to Bob's private
    resource.
-   Alice receives notifications for Bob's resource, even if the
    resource content is not directly readable.
-   A user continues receiving protected notifications after their
    access has been revoked, beyond the documented revocation window.
-   A notification or subscription is routed to the wrong user, session,
    or tenant.
-   Knowledge or reuse of another session's subscription identifier
    exposes or redirects notifications.
-   Notifications disclose sensitive resource names, metadata, or
    content to an unauthorized principal.

A successful subscription acknowledgement alone is not sufficient
evidence of a vulnerability. Inspect the acknowledged filters and
demonstrate that unauthorized notifications are actually accepted or
delivered.

#### Remediation

-   Enforce authorization for every resource URI when a subscription is
    created.
-   Associate each subscription with the authenticated principal,
    tenant, and session that created it.
-   Recheck authorization when notifications are generated or delivered,
    especially where ACLs can change during a subscription's lifetime.
-   Invalidate or suppress subscriptions after access revocation,
    logout, or session expiry.
-   Ensure subscription identifiers are used only for correlation and
    are not treated as bearer authorization tokens.
-   Isolate subscription registries and event queues by principal and
    tenant.
-   Apply notification filters server-side and send only explicitly
    requested, authorized event types and resources.
-   Minimize sensitive information in notification payloads and resource
    identifiers.
-   Log authorization and routing decisions without recording secrets.

#### Evidence to Collect

-   Sanitized requests and acknowledgements for both principals.
-   Separate notification-stream captures for Alice and Bob.
-   ACL state before and after revocation.
-   Timestamps for resource updates, revocation, and notification
    delivery.
-   Relevant server-side authorization and event-routing logs.
-   A concise reproduction showing the unauthorized principal receiving
    a protected notification.

#### Suggested Mappings

-   **CWE:** CWE-862 --- Missing Authorization; CWE-863 --- Incorrect
    Authorization; CWE-639 --- Authorization Bypass Through
    User-Controlled Key (where applicable); CWE-668 --- Exposure of
    Resource to Wrong Sphere.
-   **OWASP:** OWASP API Security Top 10 API1:2023 --- Broken Object
    Level Authorization; API5:2023 --- Broken Function Level
    Authorization only where applicable.
-   **Severity:** Context-dependent. Consider the sensitivity of the
    resource and notification payload, the number of affected
    principals/tenants, and whether access persists after revocation.
-   **Test type:** Dynamic / Hybrid.

#### References

-   MCP specification and schema applicable to the protocol version
    under test.
-   Target server documentation for resource subscriptions,
    authentication, and authorization.
-   Related test: `MCPSTG-RSRC-06` --- resource/path existence
    disclosure via subscription errors.
