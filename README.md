# Journey Mapper

A Claude Code skill that scans any codebase and generates a self-contained HTML service-design journey map — no manual diagram work required.

The output is an NN/g combined **customer journey map + service blueprint** in a single browser-ready HTML file. Open it, annotate it, share it. No server, no build step, no dependencies beyond a browser.

---

## What it does

Point it at a codebase. The skill reads your routes, components, API calls, email templates, and error states, then thinks like a service designer: who are the actors, what are their goals, what do they do and feel at each moment?

Every inferred value is flagged `[Assumption]` so you know exactly what needs validating with real users. The Frontstage, Backstage, and Support rows are sourced directly from the code — named components, real API calls, actual services.

---

## Install

### Via the Claude Code plugin marketplace

```
/plugin marketplace add joeyvansommeren/journey-mapper
/plugin install journey-mapper@journey-mapper
```

This registers the repo as a marketplace and installs the skill. To update later:

```
/plugin marketplace update
```

### Manual install

```bash
git clone https://github.com/joeyvansommeren/journey-mapper
cp -r journey-mapper/skills/journey-mapper ~/.claude/skills/journey-mapper
```

For a personal install (not project-level):

```bash
cp -r journey-mapper/skills/journey-mapper ~/.claude-personal/skills/journey-mapper
```

---

## Usage

Open any Claude Code session with a codebase in scope and run:

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

**AI fills in (read-only):**
Doing · Frontstage · Backstage · Support processes

**You fill in (editable):**
Thinking · Feeling · Pain points · Opportunities · Evidence · Notes

---

## Customising the template

The visual design lives in `skills/journey-mapper/TEMPLATE.html`. Edit the CSS variables in `:root` to match your brand — the AI only ever replaces the JSON data block inside the file, so your styling changes are safe.

Default palette: warm stone neutrals, amber accent (`#fcd34d`), Inter typeface.

---

## Staying up to date

The skill is versioned in `marketplace.json`. To pull the latest:

```bash
cd ~/Documents/journey-mapper  # or wherever you cloned it
git pull
cp -r skills/journey-mapper ~/.claude/skills/journey-mapper
```

Or if installed via the marketplace, `/plugin marketplace update` handles it.

---

## Suggesting improvements

Issues are very welcome — if something doesn't work, a journey type isn't covered, or you have an idea for the template, open one. I review suggestions and implement what fits.

PRs: open an issue first so we can discuss the approach. I keep the keys to `main` for now, but good ideas will make it in.

---

## Skill index

| Skill | Invocation | What it does |
|---|---|---|
| journey-mapper | `/journey-mapper` | Scans a codebase and generates a complete HTML journey map |

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
