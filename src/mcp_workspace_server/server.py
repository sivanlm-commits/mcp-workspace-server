from pathlib import Path
import os

from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Workspace Tools")

# Restrict access to one workspace directory
WORKSPACE_ROOT = Path(
    os.environ.get("MCP_WORKSPACE_ROOT", "./workspace")
).resolve()


def safe_path(relative_path: str) -> Path:
    """Resolve a path and ensure it stays inside the workspace."""
    candidate = (WORKSPACE_ROOT / relative_path).resolve()

    try:
        candidate.relative_to(WORKSPACE_ROOT)
    except ValueError:
        raise ValueError("Path is outside the permitted workspace.")

    return candidate


@mcp.tool()
def list_workspace_files() -> list[str]:
    """List files available inside the workspace."""
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)

    return sorted(
        str(path.relative_to(WORKSPACE_ROOT))
        for path in WORKSPACE_ROOT.rglob("*")
        if path.is_file()
    )


@mcp.tool()
def read_text_file(path: str, max_chars: int = 12000) -> str:
    """Read a UTF-8 text file from the workspace."""
    file_path = safe_path(path)

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    if max_chars < 1 or max_chars > 50000:
        raise ValueError("max_chars must be between 1 and 50000.")

    text = file_path.read_text(encoding="utf-8")
    return text[:max_chars]


@mcp.tool()
def search_text(query: str, max_results: int = 20) -> list[dict]:
    """Search text files in the workspace and return matching lines."""
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    results = []

    for file_path in WORKSPACE_ROOT.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for line_number, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                results.append(
                    {
                        "file": str(file_path.relative_to(WORKSPACE_ROOT)),
                        "line": line_number,
                        "text": line.strip(),
                    }
                )

                if len(results) >= max_results:
                    return results

    return results


def main():
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    mcp.run()


if __name__ == "__main__":
    main()
