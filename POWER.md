---
name: "pty-manager"
displayName: "PTY Session Manager"
description: "Manage multiple interactive terminal sessions (gdb, psql, etc.) through PTY. Create sessions, send commands, and read output from any interactive CLI tool."
keywords: ["pty", "terminal", "gdb", "psql", "interactive", "debugger", "repl"]
author: "tllarraz"
---

# PTY Session Manager

Manage multiple interactive terminal sessions simultaneously. Start gdb, psql, python, or any interactive CLI tool and communicate with them through a simple interface.

## Tools

- `create_session(command, timeout)` - Start a new session with any command
- `send_command(session_id, command, timeout)` - Send input to a session, get output
- `read_output(session_id, timeout)` - Read pending output without sending anything
- `list_sessions()` - Show all active sessions
- `close_session(session_id)` - Terminate a session

## Examples

### GDB Debugging

```
create_session("gdb ./myprogram")
send_command("<session_id>", "break main")
send_command("<session_id>", "run")
send_command("<session_id>", "next")
send_command("<session_id>", "print myvar")
```

### PostgreSQL

```
create_session("psql -d mydb")
send_command("<session_id>", "\\dt")
send_command("<session_id>", "SELECT * FROM users LIMIT 5;")
```

### Multiple Sessions

You can run multiple sessions at once - debug in gdb while querying postgres.

## Requirements

- `uv` / `uvx` installed
- Python 3.10+ (handled automatically by uvx)
