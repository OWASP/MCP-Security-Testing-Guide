# MCP Security Checklist

Use this checklist when auditing MCP server deployments.

## Server Configuration

- [ ] Transport encryption (TLS) enforced
- [ ] Authentication required for all connections
- [ ] Authorization scopes minimal per tool
- [ ] Rate limiting configured
- [ ] Logging captures invocations without secrets
- [ ] Error messages don't leak internals

## Tool Definitions

- [ ] Tool descriptions are static (not user-controlled)
- [ ] Input schemas validate strictly
- [ ] No shell metacharacters in arguments
- [ ] Path arguments resolved to canonical form
- [ ] File access restricted to allowed directories
- [ ] Network access restricted to allowed hosts

## Data Flow

- [ ] User consent required for sensitive operations
- [ ] Cross-server data transfer logged
- [ ] No credential forwarding between servers
- [ ] Tool outputs sanitized before passing to other tools
- [ ] Conversation history not exposed to servers

## Prompt Injection Resistance

- [ ] Tool descriptions can't be modified by attackers
- [ ] Tool outputs with instructions are flagged
- [ ] System prompt isolation between servers
- [ ] Instruction-following in outputs tested and blocked

## Deployment

- [ ] Server runs with minimal OS permissions
- [ ] Containerized with resource limits
- [ ] Network segmentation from sensitive services
- [ ] Regular dependency updates
- [ ] Incident response plan for compromised servers
