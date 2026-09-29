# local-mac-helper (STDIO MCP server)

A separate, local-only MCP server. Claude launches it as a subprocess and
talks to it over stdin/stdout. It has no network listener and no AWS parts.

Tools: `get_system_info`, `list_files` (confined to `~/Documents`, or
`MAC_HELPER_ROOT`), `add_note`, `list_notes` (stored in
`~/.local-mac-helper-notes.json`).

## Run / test

    .venv/bin/mcp dev stdio_server/server.py     # MCP Inspector

## Claude Code

    claude mcp add local-mac-helper -- "/Users/jlunde/mcp demo/.venv/bin/python" "/Users/jlunde/mcp demo/stdio_server/server.py"

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

    {
      "mcpServers": {
        "local-mac-helper": {
          "command": "/Users/jlunde/mcp demo/.venv/bin/python",
          "args": ["/Users/jlunde/mcp demo/stdio_server/server.py"]
        }
      }
    }

Restart Claude Desktop afterwards.
