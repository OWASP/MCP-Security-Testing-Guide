# How to run the tests

The assessment workflow the tests in this folder are written for: from inventory to evidence.

Use this with the [chapter overview](<3. MCP Threats and Attack Patterns.md>) (which links every category), [About the tests](about-docs-tests.md) (how the documentation is organised), and [Appendix C — Security Review](<../09. Appendix C - Security Review.md>) (review status values, scorecard and template).

## 0. Authorisation and safety

Before anything runs: written authorization covering the named systems, a lab environment for anything destructive, placeholders from [Appendix D — Safe Lab Fixtures](../10. Appendix D - Safe Lab Fixtures.md) for every identifier, and a written-down blast radius for write, install, egress and approval-bypass tests. The rules of engagement checklist is in [Test case format](test-case-format.md#mcp-red-team-checklist).

## 1. Inventory (start with `INFO`)

You cannot test what you have not enumerated. Establish:

- every host and client with MCP configuration, including workspace-level config;
- every installed server: source, version, launch command, transport;
- what each server exposes — tools, resources, prompts — and the identity it runs as;
- the trust boundaries between client, server, OS and upstream APIs;
- what context reaches the model.

Output: the data model for the rest of the assessment. Discovery here is what turns a checklist run into a real one.

## 2. Scope and prioritisation

Rank what you found by blast radius — data class, action type (read / write / delete / execute / network / credential), and reachability. Then choose categories:

| Situation | Start with |
| --- | --- |
| Never assessed before | `INFO` → `CONF` → `AUTHN`/`AUTHZ` |
| Local desktop / IDE servers | `CONF`, `AUTHZ`, `SECR` |
| Remote or multi-user deployment | `AUTHN`, `TRNS`, `GW`, `GOV` |
| Third-party or registry-installed servers | `SUPP`, `TOOL` |
| Agentic workflows with write or send capability | `AGNT`, `AUTHZ`, `TOOL` |
| Already compromised, or acting on an alert | `LOG`, then the category the alert points at |

The `Common test chains` section of each category file shows which tests are usually run together; use those rather than working top-to-bottom through every table.

## 3. Baseline

Before running a test, capture the state it will change: the tool list and schemas, the relevant configuration, the policy in force, and the log window. The first runtime test in a category is often the baseline capture itself.

## 4. Run the tests

Work one test block at a time, in the order the file presents it:

1. Read `Summary` and `Scenario` to confirm the test matches what you actually found.
2. Confirm `Preconditions`; if they are not met, record the test as **Not tested** rather than forcing it.
3. Execute `How to Test` with synthetic data only.
4. Compare against `Expected Results` — the secure case, not just the vulnerable one.
5. If the vulnerable case reproduced, apply `Remediation` in the lab and re-run to confirm the fix.

Stop conditions from step 0 override the test plan.

## 5. Evidence

For each test record: the identifier, the observation, the raw request and response (or the log excerpt), the identity used, the timestamp, the configuration state, and the policy decision. Redact secrets. An unrecorded test is not a result.

## 6. Report

Report through the [finding template](test-case-format.md#mcp-red-team-finding-template): title, test ID, affected component, attack path, impact, framework mapping, evidence, fix guidance, detection guidance, severity. Review status values and the scorecard are in [Appendix C — Security Review](<../09. Appendix C - Security Review.md>).

Where the same weakness appears in several systems, report it once with the affected systems listed — do not file one finding per host.

## 7. Retest and drift

Re-run the tests that failed once remediation lands, and re-run the `INFO` and `SUPP` tests whenever servers are installed, updated or re-sourced. A server whose tool list, schema or description changed has invalidated the earlier result.
