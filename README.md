# PTY Manager MCP Server

An MCP server that lets AI agents control interactive terminal applications like gdb, psql, python REPLs, and any other CLI tool that requires back-and-forth interaction.

## The Problem

AI coding assistants can run shell commands, but they can't interact with programs that need ongoing input. Try asking an AI to debug with gdb or run SQL queries in psql - it can start the program but can't send follow-up commands.

## The Solution

This MCP server manages PTY sessions via tmux, allowing agents to:
- Start interactive programs
- Send commands and receive output
- Maintain multiple concurrent sessions
- Let users watch sessions in real-time

## Installation

### As a Kiro Power

Add to your `.kiro/powers/pty-manager/mcp.json`:
```json
{
  "mcpServers": {
    "pty-manager": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/girotomas/pty-manager-mcp", "pty-manager-mcp"]
    }
  }
}
```

### Standalone
```bash
uvx --from git+https://github.com/girotomas/pty-manager-mcp pty-manager-mcp
```

### Requirements
- tmux
- Python 3.10+ (handled by uvx)
- uv/uvx

## Tools

| Tool | Description |
|------|-------------|
| `create_session(command, max_lines)` | Start a new session. Returns session_id and tmux session name |
| `send_command(session_id, command, wait, max_lines)` | Send a command, wait for output |
| `read_output(session_id, max_lines)` | Read current screen without sending anything |
| `list_sessions()` | List all active sessions |
| `close_session(session_id)` | Terminate a session |

Output is truncated to `max_lines` (default 30) to avoid flooding the AI's context window.

## Watching Sessions

Sessions run inside tmux. Users can attach read-only to watch what the AI is doing:

```bash
tmux attach -t pty_<session_id> -r
```

If already inside tmux (e.g., VS Code terminal):
```bash
unset TMUX && tmux attach -t pty_<session_id> -r
```

## Use Cases

### Debugging with GDB
```python
create_session("gdb ./myprogram")
send_command(id, "break main")
send_command(id, "run")
send_command(id, "next")
send_command(id, "print variable")
send_command(id, "bt")  # backtrace
```

### Database Queries
```python
create_session("psql -d mydb")
send_command(id, "\\dt")  # list tables
send_command(id, "SELECT * FROM users LIMIT 10;")
send_command(id, "\\d users")  # describe table
```

### Python REPL
```python
create_session("python3")
send_command(id, "import pandas as pd")
send_command(id, "df = pd.read_csv('data.csv')")
send_command(id, "df.describe()")
```

### Multiple Sessions
Run gdb and psql simultaneously - debug code while checking database state.

## How It Works

1. `create_session` spawns a detached tmux session running your command
2. `send_command` uses `tmux send-keys` to type into the session and `capture-pane` to read output
3. Users can attach to the tmux session read-only to observe
4. Output is normalized and truncated to keep AI context manageable

## License

MIT
