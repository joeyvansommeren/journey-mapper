# Journey Mapper

A Claude Code skill that scans any codebase and generates a self-contained HTML service-design journey map — no manual diagram work required.

The output is an NN/g combined **customer journey map + service blueprint** in a single browser-ready HTML file. Open it, annotate it, share it. No server, no build step, no dependencies beyond a browser.

---

## What it does

Point it at a codebase. The skill reads your routes, components, API calls, email templates, and error states, then thinks like a service designer: who are the actors, what are their goals, what do they do and feel at each moment?

Every inferred value is flagged `[Assumption]` so you know what needs validating with real users. The Frontstage, Backstage, and Support rows are sourced directly from the code — named components, real API calls, actual services.

---

## Install

### Claude Code — via plugin marketplace

```
/plugin marketplace add joeyvansommeren/journey-mapper
/plugin install journey-mapper@journey-mapper
```

Update later with `/plugin marketplace update`.

### Claude Code — manual

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.claude/skills/journey-mapper
```

For a personal install: use `~/.claude-personal/skills/journey-mapper` instead.

---

### OpenCode

Drop the skill files into your global commands directory:

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.config/opencode/commands/journey-mapper
```

Invoke with `/journey-mapper` in the OpenCode TUI.

For project-level install, copy to `.opencode/commands/journey-mapper` in your repo root instead.

---

### Codex CLI (OpenAI)

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp journey-mapper/skills/journey-mapper/SKILL.md ~/.codex/prompts/journey-mapper.md
cp journey-mapper/skills/journey-mapper/TEMPLATE.html ~/.codex/
cp journey-mapper/skills/journey-mapper/REFERENCE.md ~/.codex/
```

Invoke with `/journey-mapper` in Codex. Note: Codex only reads top-level `.md` files from `~/.codex/prompts/` — the SKILL.md references TEMPLATE.html by path, so keep both in `~/.codex/`.

---

### Cursor

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.cursor/commands/journey-mapper
```

Invoke by typing `/journey-mapper` in the Agent input. Cursor will show it in the dropdown.

For project-level: copy to `.cursor/commands/journey-mapper` in your repo root.

---

### Windsurf

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.codeium/windsurf/global_workflows/journey-mapper
```

Invoke with `/journey-mapper` in Cascade.

For project-level: copy to `.windsurf/workflows/journey-mapper` in your repo root.

---

### Continue.dev

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
mkdir -p ~/.continue/prompts
cp journey-mapper/skills/journey-mapper/SKILL.md ~/.continue/prompts/journey-mapper.prompt
cp journey-mapper/skills/journey-mapper/TEMPLATE.html ~/.continue/
cp journey-mapper/skills/journey-mapper/REFERENCE.md ~/.continue/
```

Invoke with `/journey-mapper` in the Continue sidebar.

---

### Gemini CLI

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
mkdir -p ~/.gemini/commands
```

Create `~/.gemini/commands/journey-mapper.toml`:

```toml
description = "Scans a codebase and generates a self-contained HTML service-design journey map."
prompt = """
[paste the contents of skills/journey-mapper/SKILL.md here]
"""
```

Invoke with `/journey-mapper` in Gemini CLI.

---

### Aider

Aider does not support custom slash commands. Use `/load` to run the skill as a prompt file:

```bash
/load path/to/journey-mapper/skills/journey-mapper/SKILL.md
```

---

## Usage

Open a session with a codebase in scope and run:

```
/journey-mapper
```

If the codebase path isn't clear from context, the skill asks. You can also be explicit:

```
/journey-mapper Scan src/ and save the output to docs/journey-map.html
```

---

## Output

A single `.html` file you can open in any browser:

- **Left rail** — all journeys grouped by category, sticky navigation
- **Journey grid** — NN/g combined customer journey + service blueprint per journey
- **Emotion curve** — renders automatically once feelings are set on two or more moments
- **Export / Import** — JSON-based annotation sharing for team collaboration
- **localStorage autosave** — all edits persist between browser sessions
- **Help modal** — press `?` for a usage guide

**AI fills in (read-only):** Doing · Frontstage · Backstage · Support processes

**You fill in (editable):** Thinking · Feeling · Pain points · Opportunities · Evidence · Notes

---

## Customising the template

The visual design lives in `skills/journey-mapper/TEMPLATE.html`. Edit the CSS variables in `:root` to match your brand. The AI only ever replaces the JSON data block, so your styling changes are safe.

Default palette: warm stone neutrals, amber accent (`#fcd34d`), Inter typeface.

---

## Staying up to date

```bash
cd ~/wherever-you-cloned-it
git pull
cp -r skills/journey-mapper ~/.claude/skills/journey-mapper   # adjust path for your agent
```

Via the Claude Code plugin marketplace: `/plugin marketplace update`.

---

## Suggesting improvements

Issues are welcome — if something doesn't work, a journey type isn't covered, or you have an idea for the template, open one. I review suggestions and implement what fits.

PRs: open an issue first. I keep the keys to `main` for now, but good ideas will make it in.

---

## Skill index

| Skill | Invocation | What it does |
|---|---|---|
| journey-mapper | `/journey-mapper` | Scans a codebase and generates a complete HTML journey map |

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
