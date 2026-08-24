# MCP Workspace Server

A lightweight Python MCP server that gives AI agents safe, structured access to files inside a controlled local workspace.

## Overview

AI agents often need access to project context stored in local files. Giving an agent unrestricted filesystem access introduces unnecessary security risk.

This project uses the Model Context Protocol (MCP) to expose a small set of controlled workspace tools while restricting access to a configured directory.

## MCP Tools

The server exposes three tools:

### `list_workspace_files`
Lists the files available inside the configured workspace.

### `read_text_file`
Reads UTF-8 text files with configurable size limits.

### `search_text`
Searches workspace documents and returns matching filenames, line numbers, and text.

## Security

The server resolves requested paths against a defined workspace root and prevents path traversal outside that directory.

Additional safeguards include:

- Restricted workspace access
- Input validation
- File-size limits
- UTF-8 handling
- Path traversal protection
- Automated security tests

## Project Structure

```text
mcp-workspace-server/
├── src/
│   └── mcp_workspace_server/
│       ├── __init__.py
│       └── server.py
├── tests/
│   └── test_paths.py
├── workspace/
│   └── example.txt
├── pyproject.toml
└── README.md
