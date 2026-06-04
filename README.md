# Journey Mapper

A Claude Code skill that scans any codebase and generates a self-contained HTML service-design journey map — no manual diagram work required.

The output is an NN/g combined **customer journey map + service blueprint** in a single browser-ready HTML file. Drop it in a project folder, open it in a browser, and you have an editable, annotatable map of every user journey the code actually implements.

---

## What it does

Point it at a codebase. The skill reads your routes, components, API calls, email templates, and error states, then thinks like a service designer: who are the actors, what are their goals, what do they do, see, and feel at each moment?

Every inferred value is flagged `[Assumption]` so you know exactly what needs validation against real users. The Frontstage, Backstage, and Support rows are sourced directly from the code — named components, real API calls, actual services.

The HTML file is self-contained. No server. No build step. Open it from a USB stick if you like.

---

## Installation

### Via the Claude Code plugin registry

```
/plugin marketplace add https://github.com/joeyvansommeren/journey-mapper
/plugin install journey-mapper@journey-mapper
```

### Manual install

Clone the repo and copy the skill files into your Claude Code skills directory:

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.claude/skills/journey-mapper
```

Or, for a personal install (Claude Code personal config):

```bash
cp -r journey-mapper/skills/journey-mapper ~/.claude-personal/skills/journey-mapper
```

---

## Usage

In any Claude Code session, with a codebase in scope:

```
/journey-mapper
```

Or invoke it directly and pass context:

```
/journey-mapper Scan the src/ directory and save the output to docs/journey-map.html
```

If the codebase path isn't clear from context, the skill will ask.

---

## Output

A single `.html` file you can open in any browser. It includes:

- **Left rail** — all journeys grouped by category, sticky navigation
- **Journey grid** — NN/g combined customer journey + service blueprint per journey
- **Emotion curve** — auto-renders once feelings are set on two or more moments
- **Export / Import** — JSON-based annotation sharing for team collaboration
- **localStorage autosave** — all edits persist in the browser between sessions
- **Help modal** — `?` key opens a usage guide

Editable fields (filled by the human after AI generates the scaffold):
- Scenario and user goal (per journey)
- Thinking (per moment)
- Feeling — emoji picker, 1–5 scale
- Pain points
- Opportunities
- Evidence — link to research artefacts
- Notes — free-form per journey

Read-only fields (filled by the AI from the codebase):
- Doing, Frontstage, Backstage, Support processes

---

## Skill index

| Skill | Invocation | What it does |
|---|---|---|
| journey-mapper | `/journey-mapper` | Scans a codebase and generates a complete HTML journey map |

---

## Customising the template

The visual design lives in `skills/journey-mapper/TEMPLATE.html`. Edit the CSS variables in `:root` to match your brand. The AI replaces only the `<script type="application/json" id="journeys-data">` block — everything else is yours to adjust.

Default palette: warm stone neutrals, amber accent (`#fcd34d`), Inter typeface.

---

## How it works

1. Dispatches an Explore subagent (or targeted grep sweeps) to extract routes, components, API endpoints, email templates, and error states from the codebase.
2. Organises the findings into actors, categories, journeys, stages, and moments following the NN/g combined journey map + service blueprint structure.
3. Generates a JSON data block and splices it into `TEMPLATE.html`.
4. Writes the complete file to disk and reports back with coverage notes and standout pain points.

See `skills/journey-mapper/REFERENCE.md` for the full JSON schema, NN/g methodology notes, and emotional arc heuristics.

---

## Requirements

- Claude Code (any recent version with plugin support)
- A codebase to scan — any language or framework

---

## Contributing

Issues and PRs are welcome. If you improve the template design, the NN/g methodology notes, or the scanning heuristics, please open a PR.

The skill is intentionally stack-agnostic. Avoid adding framework-specific logic to `SKILL.md` — put heuristics in `REFERENCE.md` where they can be extended without changing the core workflow.

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
