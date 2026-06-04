# Journey Mapper — Reference

## JSON schema

```json
{
  "actors": [
    {
      "id": "kebab-case-id",
      "name": "Display name",
      "description": "One sentence about this user type."
    }
  ],
  "categories": [
    { "id": "kebab-case-id", "title": "Display title" }
  ],
  "journeys": [
    {
      "id": "kebab-case-id",
      "title": "Human-readable journey title",
      "actor": "actor-id",
      "category": "category-id",
      "scenario": "2–3 sentence description: who this user is and what is bringing them here.",
      "goal": "One sentence — what success looks like for them.",
      "stages": [
        {
          "title": "Stage name",
          "moments": [
            {
              "id": "unique-moment-id",
              "title": "Short moment title",
              "doing": "What the user physically does.",
              "thinking": "[Assumption] What they are thinking at this point.",
              "feeling": 3,
              "pain": "[Assumption] What hurts here.",
              "opportunity": "[Assumption] What could be improved.",
              "evidence": "",
              "frontstage": "What they see: UI component, email, native prompt.",
              "backstage": "What the code does behind the scenes.",
              "support": "Which system or service underpins this."
            }
          ]
        }
      ]
    }
  ]
}
```

**Schema rules:**
- All `id` values must be unique within their array and use kebab-case.
- `moment.id` values must be stable — they key user annotations in localStorage. Do not change them after first publish.
- `feeling` is an integer 1–5. Omit the field entirely if unknown (renders as unset).
- Set `evidence` to `""` — leave it for the human to fill from real research.
- Every inferred value must be prefixed with `[Assumption]` so the human knows what needs validation.

---

## NN/g combined journey map + service blueprint

This tool implements the Nielsen Norman Group format that layers a customer journey map on top of a service blueprint, sharing the same stage/moment columns.

### Customer journey (top half of grid)

| Row | What to put here |
|---|---|
| **Doing** | Observable actions the user takes. Source directly from code (route transitions, form submissions, button clicks). Factual. |
| **Thinking** | Internal monologue. Prefix with `[Assumption]`. Infer from UX anti-patterns in the code — long forms, confusing labels, lack of confirmation. |
| **Feeling** | Emotional state 1–5. See heuristics below. |
| **Pain points** | Friction or frustration at this moment. Prefix with `[Assumption]`. |
| **Opportunities** | Design improvements. Prefix with `[Assumption]`. Keep actionable. |
| **Evidence** | Leave blank. The human fills this from user research — session recordings, Dovetail insights, support tickets, Hotjar clips. |

### Service blueprint (bottom half of grid)

| Row | What to put here |
|---|---|
| **Frontstage** | Everything the user directly sees or interacts with: specific component names, email template name, native OS dialog. |
| **Backstage** | Code and processes invisible to the user: API calls, data transforms, background jobs, state transitions. Name the actual functions or services where known. |
| **Support processes** | Infrastructure, third-party services, platform APIs that underpin the backstage. e.g. AWS SES, Stripe, Google Admin SDK. |

### The three divider lines

1. **Line of interaction** — separates Doing/Thinking/Feeling from Frontstage
2. **Line of visibility** — separates Frontstage from Backstage
3. **Line of internal interaction** — separates Backstage from Support processes

---

## Emotional arc heuristics

Use the codebase as signal to infer `feeling` scores:

| Codebase signal | Inferred score |
|---|---|
| Redirect chain of 3+ hops | 2 |
| Error state with no clear recovery path | 1 |
| Empty state with no next-step guidance | 2 |
| Complex multi-step form (5+ fields) | 2 |
| Long loading spinner with no ETA or progress | 2 |
| Opaque permission prompt (Accessibility, camera, etc.) | 1–2 |
| First successful action / success confirmation screen | 4 |
| Single-click action with instant feedback | 4 |
| Access granted after a gate or block | 4–5 |
| Cold landing — user has no prior context | 1–2 |
| Returning user, familiar flow, no changes | 3–4 |
| SSO or magic-link (fast, low friction) | 4 |

When in doubt, use 3 (neutral) for unknown moments. The human adjusts from real research.

---

## Structural guidance

- **4–12 journeys** per file — fewer is better. Cover the golden path first, then edge/recovery paths.
- **2–5 stages per journey** — each stage name should be a short verb phrase (Discover, Sign up, Verify, Land).
- **2–4 moments per stage** — if a stage has more than 4, consider splitting it.
- **Cover all actors** — every actor type should appear in at least one journey.
- **Cover error/recovery** — the happy path alone is not a service design.
- **Name real things** — reference actual component names, file names, and API endpoints in Frontstage and Backstage. This makes the map verifiable against the codebase.

---

## Minimal worked example

```json
{
  "actors": [
    { "id": "new-user", "name": "New user", "description": "Someone creating their first account." }
  ],
  "categories": [
    { "id": "onboarding", "title": "Onboarding" }
  ],
  "journeys": [
    {
      "id": "sign-up",
      "title": "Create an account",
      "actor": "new-user",
      "category": "onboarding",
      "scenario": "A prospective user has discovered the product and wants to create an account to try it.",
      "goal": "Get from zero to a working account with access to the core feature.",
      "stages": [
        {
          "title": "Sign up",
          "moments": [
            {
              "id": "land-signup",
              "title": "Lands on the signup page",
              "doing": "Arrives from a referral link and sees the signup form.",
              "thinking": "[Assumption] Is this going to take long? Can I look around first?",
              "feeling": 3,
              "pain": "[Assumption] No way to preview the product before committing to an account.",
              "opportunity": "[Assumption] Offer a sandbox or quick demo before requiring signup.",
              "evidence": "",
              "frontstage": "SignUp form: email, name, password. Google/Microsoft SSO buttons.",
              "backstage": "Static React build served from CDN. No API calls yet.",
              "support": "CloudFront CDN."
            }
          ]
        }
      ]
    }
  ]
}
```
