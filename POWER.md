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

Use the `tmux_session` value from the response.

## Tools

### create_session(command, max_lines=30)
Start a new interactive session.

- `command`: The command to run (e.g., "gdb ./myprogram", "psql -d mydb")
- `max_lines`: Truncate initial output to this many lines (default 30)

Returns: `session_id`, `tmux_session`, `attach_command`, `output`, `total_lines`

### send_command(session_id, command, wait=1.0, max_lines=30)
Send a command to a session and get output.

- `session_id`: From create_session response
- `command`: Text to send (will press Enter after)
- `wait`: Seconds to wait for output (default 1.0). Increase for slow commands.
- `max_lines`: Truncate output to this many lines. Use higher values (100+) for large outputs like backtraces.

Returns: `output`, `total_lines`

### read_output(session_id, max_lines=30)
Read current screen without sending anything. Useful to check if a long-running command finished.

### list_sessions()
List all active sessions with their tmux names.

### close_session(session_id)
Terminate a session.

## Tips

- If output says `total_lines: 150` but you only see 30, increase `max_lines` to see more
- For slow commands (compilation, large queries), increase `wait`
- Use `read_output` to poll for completion without sending input

## Requirements

- tmux
- uvx
