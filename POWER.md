---
name: "pty-manager"
displayName: "PTY Session Manager"
description: "Manage multiple interactive terminal sessions (gdb, psql, etc.) through PTY. Create sessions, send commands, and read output from any interactive CLI tool."
keywords: ["pty", "terminal", "gdb", "psql", "interactive", "debugger", "repl"]
author: "girotomas"
---

# PTY Session Manager

Manage multiple interactive terminal sessions simultaneously. Start gdb, psql, python, or any interactive CLI tool and communicate with them through a simple interface.

## Watching Sessions

Sessions run inside tmux. After creating a session, tell the user they can watch it live:

```
tmux attach -t <tmux_session> -r
```

If inside VS Code's terminal (nested tmux), use:
```
unset TMUX && tmux attach -t <tmux_session> -r
```

The `-r` flag makes it read-only so the user can watch without interfering.

## Tools

- `create_session(command, max_lines)` - Start a new session, returns `tmux_session` name for attaching
- `send_command(session_id, command, wait, max_lines)` - Send input, get output (truncated to max_lines, default 30)
- `read_output(session_id, max_lines)` - Read current screen content
- `list_sessions()` - Show all active sessions
- `close_session(session_id)` - Terminate a session

## Requirements

- tmux installed
- `uv` / `uvx` installed
