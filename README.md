# OWASP MCP Security Testing Guide

The Model Context Protocol (MCP) is an open protocol that lets LLM applications connect to external data sources, tools, prompts, workflows, and services. This guide treats MCP as a security boundary: the chain from the user, through the model and MCP client, to the MCP server, the connected tool, and the target system.

It is a living collection of MCP security knowledge for developers, AppSec, red teams, and SOC teams. It covers threats, secure development, host and client controls, supply chain, enterprise gateways, detection, incident response, taxonomy, public incidents, case studies, and review checklists. Host and client controls are in [Chapter 3](<03. MCP Threats and Attack Patterns/3. MCP Threats and Attack Patterns.md#host-and-client-baseline>).

This work is licensed under [GPL-3.0](LICENSE).

## Chapters

Read the guide in this order. Chapter 3 holds the threat write-ups and **79 tests** in sections 3.1–3.19. 

1. [Project Overview](<01. Project_Overview.md>)
2. [MCP Fundamentals](<02. MCP Fundamentals.md>)
3. [MCP Threats and Attack Patterns](<03. MCP Threats and Attack Patterns/3. MCP Threats and Attack Patterns.md>)
4. [Secure MCP Development](<04. Secure MCP Development.md>)
5. [MCP Security Taxonomy](<05. MCP Security Taxonomy.md>)
6. [Hacks, News, and Public Incidents](<06. Hacks, News, and Public Incidents.md>)
7. [Appendix A — Glossary](<07. Appendix A - Glossary.md>)
8. [Appendix B — Suggested Reading](<08. Appendix B - Suggested Reading.md>)
9. [Appendix C — Security Review](<09. Appendix C - Security Review.md>)
10. [Appendix D — Safe Lab Fixtures](<10. Appendix D - Safe Lab Fixtures.md>)
11. [Appendix F — Testing Tools](<11. Appendix F - Testing Tools.md>)


Do not use it to test systems without explicit written authorization. Use synthetic lab environments and placeholders or try this [MCP Goat](https://github.com/mcp-security-project/mcp-goat)

## Related OWASP projects

- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)

Appendix E is unused so the Appendix D and Appendix F links already used by the Chapter 3 tests stay stable. Report a finding with the [finding template](<03. MCP Threats and Attack Patterns/test-case-format.md#mcp-red-team-finding-template>) and [Appendix C](<09. Appendix C - Security Review.md#mcp-security-review-template>).
