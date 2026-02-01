#!/usr/bin/env python3
import uuid
import pexpect
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pty-manager")

sessions: dict[str, pexpect.spawn] = {}


@mcp.tool()
def create_session(command: str, timeout: int = 30) -> dict:
    """Create a new PTY session with the given command."""
    session_id = str(uuid.uuid4())[:8]
    try:
        child = pexpect.spawn(command, encoding='utf-8', timeout=timeout)
        child.setwinsize(40, 200)
        sessions[session_id] = child
        
        try:
            child.expect(pexpect.TIMEOUT, timeout=1)
        except pexpect.TIMEOUT:
            pass
        
        initial_output = child.before or ""
        return {
            "session_id": session_id,
            "status": "created",
            "output": initial_output
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def send_command(session_id: str, command: str, timeout: int = 10) -> dict:
    """Send a command to an existing PTY session and return the output."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    child = sessions[session_id]
    if not child.isalive():
        del sessions[session_id]
        return {"error": "Session has terminated"}
    
    try:
        child.sendline(command)
        try:
            child.expect(pexpect.TIMEOUT, timeout=timeout)
        except pexpect.TIMEOUT:
            pass
        
        output = child.before or ""
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def read_output(session_id: str, timeout: int = 2) -> dict:
    """Read any pending output from a session without sending a command."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    child = sessions[session_id]
    if not child.isalive():
        del sessions[session_id]
        return {"error": "Session has terminated"}
    
    try:
        try:
            child.expect(pexpect.TIMEOUT, timeout=timeout)
        except pexpect.TIMEOUT:
            pass
        
        output = child.before or ""
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_sessions() -> dict:
    """List all active PTY sessions."""
    result = {}
    dead = []
    for sid, child in sessions.items():
        if child.isalive():
            result[sid] = {"alive": True, "command": child.args[0] if child.args else "unknown"}
        else:
            dead.append(sid)
    
    for sid in dead:
        del sessions[sid]
    
    return {"sessions": result}


@mcp.tool()
def close_session(session_id: str) -> dict:
    """Close a PTY session."""
    if session_id not in sessions:
        return {"error": f"Session {session_id} not found"}
    
    child = sessions[session_id]
    try:
        child.terminate(force=True)
    except:
        pass
    
    del sessions[session_id]
    return {"status": "closed"}


def main():
    mcp.run()


if __name__ == "__main__":
    main()
