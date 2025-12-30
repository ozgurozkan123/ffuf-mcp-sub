import os
import subprocess
from typing import List
from fastmcp import FastMCP

# Initialize FastMCP server
title = "ffuf-mcp"
mcp = FastMCP(title)


@mcp.tool()
def do_ffuf(url: str, ffuf_args: List[str]) -> str:
    """Run ffuf with the provided URL and arguments.

    Args:
        url: Target URL to fuzz (passed to -u).
        ffuf_args: Additional ffuf CLI arguments (one per list item), e.g. ['-w', '/path/wordlist', '-mc', '200'].
    """
    command = ["ffuf", "-u", url, *ffuf_args]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return "ffuf binary not found in PATH. Ensure Docker image installs it correctly."

    output = []
    output.append(f"Command: {' '.join(command)}")
    output.append(f"Exit code: {result.returncode}")
    if result.stdout:
        output.append("--- stdout ---")
        output.append(result.stdout)
    if result.stderr:
        output.append("--- stderr ---")
        output.append(result.stderr)

    return "\n".join(output)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    mcp.run(
        transport="sse",
        host=host,
        port=port,
        path="/mcp",
    )
