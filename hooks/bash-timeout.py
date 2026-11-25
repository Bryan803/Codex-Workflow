#!/usr/bin/env python3
"""Codex PreToolUse hook for shell commands: puts a hard time limit on long-running commands.

Codex only accepts a rewritten command together with an auto-approve, which would
bypass the owner's approval prompts. So this hook denies the bare command and hands
the agent the wrapped version to run instead (approval still applies to that).

Why: a build/test can finish while a daemon it spawned (Gradle, adb, emulator)
keeps the output pipe open, so the shell call never returns and the agent waits
forever. Wrapped commands write to a log file instead of the pipe, run under
`timeout` (which kills the whole process group), and only the log tail is shown.

Which commands get wrapped:
  - foreground commands matching LONG_RUNNING
Override the limit by adding a comment to the command, e.g. `# timeout=90m`.
Skip wrapping with `# no-timeout`.
"""
import json
import re
import shlex
import sys

DEFAULT_LIMIT = "20m"
SLOW_LIMIT = "45m"  # Android builds and device tests
LONG_RUNNING = re.compile(
    r"(gradlew|\bgradle\b|\badb\b|\bemulator\b|\bnpm\s+(run|test|ci|install)|\bpnpm\b|\byarn\b|\bbun\b"
    r"|\bnpx\b|\bvitest\b|\bjest\b|\bplaywright\b|\bpytest\b|\bcargo\b|\bgo\s+(test|build)\b"
    r"|\bdocker\b|\bmake\b|\bsupabase\b|\bvercel\b|\bnext\s+build\b|\btsc\b|\btsgo\b)"
)
SLOW = re.compile(r"(gradlew|\bgradle\b|connected\w*AndroidTest|\bemulator\b|run-device-tests)")
OVERRIDE = re.compile(r"#\s*timeout=(\d+[smh]?)")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") not in ("Bash", "shell", "local_shell", "exec_command", "container.exec"):
        return
    tool_input = data.get("tool_input") or {}
    cmd = tool_input.get("command") or tool_input.get("cmd") or ""
    if isinstance(cmd, list):  # argv form, e.g. ["bash", "-lc", "..."]
        cmd = cmd[-1] if cmd and isinstance(cmd[-1], str) else ""

    if "# no-timeout" in cmd or cmd.lstrip().startswith(("timeout ", "CODEX_TIMEOUT_WRAPPED=1")):
        return

    m = OVERRIDE.search(cmd)
    if m:
        limit = m.group(1)
    elif SLOW.search(cmd):
        limit = SLOW_LIMIT
    elif LONG_RUNNING.search(cmd):
        limit = DEFAULT_LIMIT
    else:
        return  # short foreground command: the Bash tool's own 2-10 min limit applies

    wrapped = (
        'CODEX_TIMEOUT_WRAPPED=1; _d="${TMPDIR:-/tmp}/codex-cmd-logs"; mkdir -p "$_d"; '
        '_log="$_d/$(date +%Y%m%d-%H%M%S)-$$.log"; '
        f'echo "[time limit {limit}, live log: $_log]"; '
        f"timeout -k 30s {limit} bash -c {shlex.quote(cmd)} >\"$_log\" 2>&1 </dev/null; _rc=$?; "
        'tail -c 30000 "$_log"; '
        f'if [ $_rc -eq 124 ] || [ $_rc -eq 137 ]; then echo; echo "TIMED OUT after {limit} (killed). '
        'Report this; do not wait or retry blindly. Full log: $_log"; '
        'else echo; echo "[exit $_rc, full log: $_log]"; fi; exit $_rc'
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Long-running command: run it under a {limit} time limit instead. "
                "Run exactly this command (same working directory), nothing else changed:\n" + wrapped
            ),
        }
    }))


if __name__ == "__main__":
    main()
