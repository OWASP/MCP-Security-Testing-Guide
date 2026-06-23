"""MCP Security Test Client - Tool-level fuzzing and validation."""

import json
import hashlib
import secrets
from typing import Any


class MCPTestClient:
    """Minimal MCP client for security testing."""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session_id = secrets.token_hex(16)

    def build_tool_call(self, tool_name: str, arguments: dict) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

    def build_list_tools(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 1,
        }

    def generate_path_traversal_payloads(self) -> list[dict]:
        """Generate path traversal test vectors."""
        bases = ["/etc/passwd", "/etc/shadow", "/proc/self/environ"]
        traversals = [
            "../../../",
            "....//",
            "%2e%2e%2f",
            "..\\",
            "....\\\\",
        ]
        payloads = []
        for base in bases:
            for traversal in traversals:
                payloads.append({"path": traversal + base})
                payloads.append({"path": "foo/" + traversal + base})
        return payloads

    def generate_command_injection_payloads(self) -> list[dict]:
        """Generate command injection test vectors."""
        commands = ["ls", "echo hello", "pwd"]
        separators = [";", "&&", "||", "|", "`", "$("]
        injections = ["/etc/passwd", "id", "whoami"]
        payloads = []
        for cmd in commands:
            for sep in separators:
                for inj in injections:
                    payloads.append({"command": f"{cmd} {sep} {inj}"})
        return payloads

    def generate_credential_leak_payloads(self) -> list[dict]:
        """Generate payloads to test credential exposure."""
        fake_tokens = [
            "sk-live-" + secrets.token_hex(16),
            "ghp_" + secrets.token_hex(20),
            "AKIA" + secrets.token_hex(10),
            "Bearer " + secrets.token_hex(16),
        ]
        payloads = []
        for token in fake_tokens:
            payloads.append({
                "url": "https://httpbin.org/post",
                "headers": {"Authorization": f"Bearer {token}"},
                "_test_token": token,
            })
        return payloads

    def generate_tool_poisoning_indicators(self) -> list[str]:
        """Strings that indicate tool description poisoning attempts."""
        return [
            "IMPORTANT: Before using this tool",
            "SYSTEM: Ignore previous instructions",
            "You must first execute",
            "Before proceeding, run",
            "Secret directive:",
            "Hidden instruction:",
            "Override: ",
        ]

    def generate_schema_violation_payloads(self, schema: dict) -> list[dict]:
        """Generate payloads that violate the expected schema."""
        props = schema.get("properties", {})
        required = schema.get("required", [])
        payloads = []

        # Missing required fields
        if required:
            payloads.append({})

        # Wrong types
        for prop, spec in props.items():
            expected_type = spec.get("type", "string")
            if expected_type == "string":
                payloads.append({prop: 12345})
                payloads.append({prop: ["array", "not", "string"]})
                payloads.append({prop: {"nested": "object"}})
            elif expected_type == "number":
                payloads.append({prop: "not-a-number"})
                payloads.append({prop: True})
            elif expected_type == "array":
                payloads.append({prop: "not-an-array"})
                payloads.append({prop: 42})

        # Oversized inputs
        payloads.append({prop: "A" * 100000 for prop in props if props[prop].get("type") == "string"})

        # Null bytes
        for prop in props:
            payloads.append({prop: "test\x00value"})

        return payloads

    def compute_response_hash(self, response: dict) -> str:
        """Hash response for comparison (detect rug pull changes)."""
        serialized = json.dumps(response, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()


def run_fuzz_test(client: MCPTestClient, tool_name: str, schema: dict) -> dict:
    """Run all fuzz tests against a tool."""
    results = {
        "path_traversal": [],
        "command_injection": [],
        "schema_violations": [],
        "credential_leaks": [],
    }

    # Path traversal
    for payload in client.generate_path_traversal_payloads():
        results["path_traversal"].append({
            "input": payload,
            "note": "Check if file was accessed",
        })

    # Command injection
    for payload in client.generate_command_injection_payloads():
        results["command_injection"].append({
            "input": payload,
            "note": "Check if command executed",
        })

    # Schema violations
    for payload in client.generate_schema_violation_payloads(schema):
        results["schema_violations"].append({
            "input": payload,
            "note": "Check error handling",
        })

    # Credential leaks
    for payload in client.generate_credential_leak_payloads():
        results["credential_leaks"].append({
            "input": payload,
            "note": "Check logs for token exposure",
        })

    return results


if __name__ == "__main__":
    client = MCPTestClient("ws://localhost:8080")
    print(f"Test client ready for {client.server_url}")
    print(f"Session: {client.session_id}")
    print(f"Path traversal payloads: {len(client.generate_path_traversal_payloads())}")
    print(f"Command injection payloads: {len(client.generate_command_injection_payloads())}")
    print(f"Credential leak payloads: {len(client.generate_credential_leak_payloads())}")
