# PTY Manager MCP Server

MCP server for managing interactive PTY sessions. Run gdb, psql, or any interactive CLI tool and communicate with them through MCP.

## Installation

```bash
uvx --from git+https://github.com/girotomas/pty-manager-mcp pty-manager-mcp
```

## Tools

- `create_session(command)` - Start a new session
- `send_command(session_id, command)` - Send input, get output
- `read_output(session_id)` - Read pending output
- `list_sessions()` - Show active sessions
- `close_session(session_id)` - Terminate a session
