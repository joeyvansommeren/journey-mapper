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

Plugin skills are namespaced by plugin name, so a plugin install is invoked as `/journey-mapper:journey-mapper`. Claude also picks it up automatically when you ask for a journey map.

### Claude Code — manual

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.claude/skills/journey-mapper
```

A manual install is invoked as plain `/journey-mapper`. For a single project, copy it to `.claude/skills/journey-mapper` in that repo instead.

---

### Other agents — Codex, Cursor, OpenCode, Gemini CLI, GitHub Copilot, Windsurf

These tools all read [Agent Skills](https://agentskills.io) folders natively, and all of them look in the shared `.agents/skills` location. One copy covers every one of them:

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
mkdir -p ~/.agents/skills
cp -r journey-mapper/skills/journey-mapper ~/.agents/skills/journey-mapper
```

For a single project, copy it to `.agents/skills/journey-mapper` in that repo instead. Keep `REFERENCE.md` and `TEMPLATE.html` next to `SKILL.md` — the skill refers to them by relative path.

| Tool | How to invoke |
|---|---|
| Codex CLI | `$journey-mapper`, or pick it from `/skills` |
| Cursor | `/journey-mapper` in Agent chat |
| OpenCode | Ask for a journey map — it loads the skill automatically |
| Gemini CLI | Ask for a journey map and confirm activation; check with `/skills list` |
| GitHub Copilot (CLI and VS Code agent mode) | Mention `/journey-mapper` in your prompt; run `/skills reload` after installing |
| Windsurf / Devin Desktop (Cascade) | `@journey-mapper` |

Every tool also triggers the skill on its own when you ask for a journey map or service blueprint.

---

### Continue.dev

Continue reads skill folders from its own directory rather than `.agents/skills`:

```bash
mkdir -p ~/.continue/skills
cp -r journey-mapper/skills/journey-mapper ~/.continue/skills/journey-mapper
```

For a single project, use `.continue/skills/journey-mapper`.

---

### Aider

Aider has no skill support. Load the skill files read-only instead:

```bash
aider --read path/to/journey-mapper/skills/journey-mapper/SKILL.md \
      --read path/to/journey-mapper/skills/journey-mapper/REFERENCE.md
```

Then ask for a journey map, and point Aider at `TEMPLATE.html` in the same folder.

---

## Usage

Open a session with a codebase in scope and run:

```
/journey-mapper
```

(Installed via the Claude Code plugin marketplace? Use `/journey-mapper:journey-mapper`.)

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
cp -r skills/journey-mapper ~/.agents/skills/journey-mapper   # or ~/.claude/skills for Claude Code
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
