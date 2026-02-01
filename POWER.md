---
name: "pty-manager"
displayName: "PTY Session Manager"
description: "Manage multiple interactive terminal sessions (gdb, psql, etc.) through PTY. Create sessions, send commands, and read output from any interactive CLI tool."
keywords: ["pty", "terminal", "gdb", "psql", "interactive", "debugger", "repl"]
author: "girotomas"
---

# PTY Session Manager

Manage interactive terminal sessions (gdb, psql, python, etc).

## IMPORTANT: Always tell the user how to watch

After calling `create_session`, you MUST tell the user:

> You can watch this session live by running:
> `unset TMUX && tmux attach -t <tmux_session> -r`

Use the `tmux_session` value from the create_session response (e.g., `pty_abc123`).

## Tools

- `create_session(command, max_lines)` - Start session, returns `tmux_session` for attaching
- `send_command(session_id, command, wait, max_lines)` - Send input, get output
- `read_output(session_id, max_lines)` - Read current screen
- `list_sessions()` - List active sessions
- `close_session(session_id)` - Terminate session

## Requirements

- tmux
- uvx
