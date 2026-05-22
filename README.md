# skills

Public repository of the **skills** I'm using day-to-day (and skills I've helped prepare for colleagues).

> **Note:** Most skills have **built-in onboarding** — the first time you use them, they ask a few questions to learn your context (your company's brand, your role, your preferred tools) and then tailor themselves to you. You don't need to fork or edit anything; just install and go. A few skills (mainly the CETIN-branded ones) are more hardwired to a specific organizational context — those are clearly named and are best used as a starting point if you want to adapt them to your own setup.

Maintained by **Jiří Forman** — [LinkedIn](https://www.linkedin.com/in/jiriforman/).

## What are skills?

Skills are bundles of instructions (and optional helper files) that teach Claude how to do a specific task well. Drop one into **Claude Code** or **Microsoft 365 Copilot Cowork** and the model gains a new capability — it knows *when* to use the skill and *how*, so you don't have to re-explain the workflow every time.

## Skills in this repo

The table below is auto-generated from each skill's `skill.yaml` on every push to `main`. Click any `.zip` link to download a skill directly — no GitHub account needed.

<!-- skills-table:start -->
| Skill | Description | Tags | Version | Last update | Updated by | Download |
|---|---|---|---|---|---|---|
| [Company Design](skills/company-design) | Self-configuring company design system — learns a company's brand once, then applies it everywhere. Runs a one-time onboarding to extract colors, fonts, and logos from a website, uploaded files, or brand guidelines, then automatically brands every business visual deliverable (presentations, documents, dashboards, HTML/React artifacts, charts, diagrams). | `communication`, `presentation`, `branding` | `1.0.0` | 2026-05-22 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/company-design.zip) |
| [CETIN Design](skills/cetin-design) | CETIN corporate design system — applies CETIN branding (CETIN Blue + Red, Avenir/Arial, official logos, brand layouts) to visual outputs including presentations, HTML/React artifacts, dashboards, Excel charts, and Word documents. | `communication`, `presentation` | `1.3.0` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/cetin-design.zip) |
| [Idea Forge](skills/idea-forge) | AI-guided PRD intake — a structured 8-phase business analyst conversation that captures a business idea (problem, As-Is / To-Be process with Mermaid diagrams, benefits, MoSCoW requirements) and emits a Markdown PRD plus a standalone HTML preview. | `idea-specification`, `business-analysis`, `productivity` | `1.0.0` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/idea-forge.zip) |
| [Jira Report](skills/jira-report) | Generates a CETIN-branded HTML dashboard report from a JIRA CSV export — status overview, sprint/velocity metrics, aging and blocker analysis, and project/epic breakdown rendered as interactive charts and tables. | `reporting`, `process-analysis` | `1.0.0` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/jira-report.zip) |
| [Morning Brief](skills/morning-brief) | Personalized daily morning brief — covers today's calendar, important email, Teams activity, Planner tasks, and (for managers) pending items from direct reports. Delivers an inline summary with a deep link to the Planner kanban, supports multiple languages, and can be scheduled to run automatically. | `productivity` | `1.1.0` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/morning-brief.zip) |
| [RFP Evaluation](skills/rfp-evaluation) | Evaluates SaaS vendor proposals for CETIN (telco) procurement — weighted scoring matrix, vendor summaries, HTML dashboard, and shortlist memo. Always covers Security & GDPR, BSS/OSS integration, SLA/support, and Commercials & vendor viability. | `finance`, `business-analysis` | `1.0.0` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/rfp-evaluation.zip) |
| [Weekly Planning](skills/weekly-planning) | Personal weekly planning assistant — maintains a persistent task list and preferences in OneDrive, produces a past-week recap and next-week plan as concise Adaptive Card dashboards, surfaces public holidays and team OOO, and pulls priorities from line manager and direct reports. | `productivity` | `1.0.3` | 2026-05-20 | jformancz | [.zip](https://github.com/jiriforman/skills/releases/latest/download/weekly-planning.zip) |
<!-- skills-table:end -->

## Browse the catalog (web)

The catalog site mirrors the table above with search, tag filters, and richer descriptions:

**👉 [ailearning.jforman.cz/skills](https://ailearning.jforman.cz/skills)**

[![Skills catalog preview](docs/skills-catalog.png)](https://ailearning.jforman.cz/skills)

Source for the catalog site: [jiriforman/ailearningpath](https://github.com/jiriforman/ailearningpath)

## How to install a skill

### In Claude Code

1. On the [catalog page](https://ailearning.jforman.cz/skills), click **Download skill** on the one you want — you'll get a `.zip`.
2. In Claude Code, open the **Customize** panel (left side) and choose **Import skill**, pointing it at the `.zip`.
3. Alternatively: open the `.md` file inside the `.zip` and paste the text into Claude Code.

### In Microsoft 365 Copilot Cowork

1. On the [catalog page](https://ailearning.jforman.cz/skills), click **Download skill** to get the `.zip`.
2. In Cowork, upload the `.zip` to the agent and ask it to install a new skill (or paste the `.md` content directly).
3. Follow the prompts and customize the skill to your needs.

### Official references

- **Claude Code:** [official skills documentation (Anthropic)](https://docs.claude.com/en/docs/claude-code/skills)
- **M365 Copilot Cowork:** [official intro](https://learn.microsoft.com/en-us/microsoft-365-copilot/)

## Using this repo

Anyone is welcome to:

- **Fork** this repo and adapt skills for your own organization or workflow.
- **Open an issue** to suggest a new skill or report a problem with an existing one.
- **Open a pull request** to contribute a new skill or improve an existing one.

See [CONTRIBUTING.md](CONTRIBUTING.md) for a step-by-step contributor's guide (friendly to GitHub newcomers).

## Contact

Questions, feedback, or want to share a skill you've adapted? Reach out:

- **LinkedIn:** [linkedin.com/in/jiriforman](https://www.linkedin.com/in/jiriforman/)
- **Issues:** [open one here](https://github.com/jiriforman/skills/issues/new)

## License

This repository is licensed under the terms of the [LICENSE](LICENSE) file at the root of the project.
