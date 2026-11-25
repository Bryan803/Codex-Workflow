---
name: ponytail-help
description: Use only when the user explicitly requests ponytail-help by name or command.
---

Only activate when the user explicitly asks to use this Ponytail skill by name or command. Mentions while configuring or discussing skills are not activation requests. Ordinary coding tasks, simplicity requests, and complaints about complexity do not activate it.

# Ponytail Help

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/ponytail lite` | Build what was asked, name the smaller option in one line. |
| **Full** | `/ponytail` | The smallest complete change, a check where the logic needs one, and a reply that names what was skipped and any risk. Default. |
| **Ultra** | `/ponytail ultra` | Also questions the request and pushes back before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ponytail** | `/ponytail` | Lazy mode itself: least new code, clear replies that name skipped work and risks. |
| **ponytail-review** | `/ponytail-review` | Quality review of a diff: bugs, security, load, missing tests, speed, what to cut. Each finding says what goes wrong and how to fix it. |
| **ponytail-audit** | `/ponytail-audit` | The same quality review for the whole repo, ranked. |
| **ponytail-debt** | `/ponytail-debt` | Harvest `shortcut:` comments into a tracked ledger. |
| **ponytail-gain** | `/ponytail-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **ponytail-help** | `/ponytail-help` | This card. |

In Codex CLI and the IDE extension, invoke skills with `$ponytail`,
`$ponytail-review`, or `$ponytail-help`. Claude Code and OpenCode use the
slash-command forms above (OpenCode ships all six as slash commands).

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `/ponytail`.
`/ponytail off` also works.

## Band (Claude Code)

`/ponytail band` hides the band above the prompt, the same command brings it back.
`/ponytail band on` and `/ponytail band off` set it directly. The level stays.
`/ponytail band import` adds your past Claude Code sessions (cost, agent time, tokens) to the board.

## Codex installation

These are local, explicit-only Codex skills. Default mode is off. Invoke `$ponytail` to activate it for this session. The Ponytail plugin and its automatic hooks are disabled; plugin updates do not update these local copies.

## More

Full docs + examples: https://github.com/DietrichGebert/ponytail
