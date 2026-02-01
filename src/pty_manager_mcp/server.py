#!/usr/bin/env python3
import uuid
import subprocess
import time
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pty-manager")

SESSION_PREFIX = "pty_"
sessions: dict[str, str] = {}  # session_id -> tmux session name


def run_tmux(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(["tmux"] + args, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


@mcp.tool()
def create_session(command: str, timeout: int = 30) -> dict:
    """Create a new PTY session. Attach with: tmux attach -t <session_name> -r"""
    session_id = str(uuid.uuid4())[:8]
    tmux_name = f"{SESSION_PREFIX}{session_id}"
    
    code, out, err = run_tmux(["new-session", "-d", "-s", tmux_name, command])
    if code != 0:
        return {"error": f"Failed to create tmux session: {err}"}
    
    sessions[session_id] = tmux_name
    time.sleep(0.5)
    
    code, out, err = run_tmux(["capture-pane", "-t", tmux_name, "-p"])
    
    return {
        "session_id": session_id,
        "tmux_session": tmux_name,
        "attach_command": f"tmux attach -t {tmux_name} -r",
        "output": out.strip()
    }


@mcp.tool()
def send_command(session_id: str, command: str, timeout: int = 10) -> dict:
    """Send a command to a session and return output."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    tmux_name = sessions[session_id]
    
    code, _, err = run_tmux(["send-keys", "-t", tmux_name, command, "Enter"])
    if code != 0:
        return {"error": f"Failed to send command: {err}"}
    
    time.sleep(min(timeout, 2))
    
    code, out, err = run_tmux(["capture-pane", "-t", tmux_name, "-p"])
    if code != 0:
        return {"error": f"Failed to capture output: {err}"}
    
    return {"output": out.strip()}


@mcp.tool()
def read_output(session_id: str, timeout: int = 2) -> dict:
    """Read current screen content from a session."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    tmux_name = sessions[session_id]
    
    code, out, err = run_tmux(["capture-pane", "-t", tmux_name, "-p"])
    if code != 0:
        return {"error": f"Failed to capture output: {err}"}
    
    return {"output": out.strip()}


@mcp.tool()
def list_sessions() -> dict:
    """List all active PTY sessions."""
    code, out, err = run_tmux(["list-sessions", "-F", "#{session_name}"])
    
    if code != 0:
        return {"sessions": {}}
    
    active = {}
    for line in out.strip().split("\n"):
        if line.startswith(SESSION_PREFIX):
            sid = line[len(SESSION_PREFIX):]
            if sid in sessions:
                active[sid] = {"tmux_session": line, "attach": f"tmux attach -t {line} -r"}
    
    return {"sessions": active}


@mcp.tool()
def close_session(session_id: str) -> dict:
    """Close a PTY session."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    tmux_name = sessions[session_id]
    run_tmux(["kill-session", "-t", tmux_name])
    del sessions[session_id]
    
    return {"status": "closed"}


def main():
    mcp.run()


if __name__ == "__main__":
    main()
