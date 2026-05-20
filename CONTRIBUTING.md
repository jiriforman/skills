# Contributing

Thanks for your interest in contributing! This guide walks you through the process from start to finish. **No prior GitHub experience required** — if you get stuck, open an issue and ask.

## Ways to contribute

- 🐛 **Report a problem** with an existing skill → [open an issue](https://github.com/jiriforman/skills/issues/new)
- 💡 **Suggest a new skill** → open an issue describing the use case
- ✍️ **Improve an existing skill** → open a pull request with your edits
- ➕ **Add a brand-new skill** → open a pull request with the new files

## Quick start: contributing via the GitHub website (no terminal needed)

If you only want to tweak a file, the easiest path is straight in your browser:

1. Click the **Fork** button at the top right of [this repo](https://github.com/jiriforman/skills). This creates your own copy under your GitHub account.
2. In your fork, navigate to the file you want to change and click the **pencil icon** (Edit).
3. Make your changes. GitHub will commit them to a new branch on your fork.
4. At the top of the page, click **Contribute → Open pull request**.
5. Add a short title and description explaining your change.
6. Submit — the repo maintainer will review and merge.

## Full workflow: contributing with git locally

For larger changes (multiple files, new skills with attachments, etc.):

### 1. Fork and clone

```bash
# Click "Fork" on github.com/jiriforman/skills first, then:
git clone https://github.com/<your-username>/skills.git
cd skills
git remote add upstream https://github.com/jiriforman/skills.git
```

### 2. Create a branch

Always work on a new branch — never directly on `main`:

```bash
git checkout -b my-new-skill
```

Use a short, descriptive branch name (e.g. `add-meeting-notes-skill`, `fix-rfp-typo`).

### 3. Make your changes

- Add or edit files.
- If you're adding a new skill, follow the structure of existing skills in the repo (a `SKILL.md` plus any helper files, optionally bundled as a `.zip`).
- Test the skill in Claude Code or Cowork before submitting.

### 4. Commit

```bash
git add .
git commit -m "Add meeting-notes skill"
```

Keep commit messages short and descriptive (imperative mood: "Add X", "Fix Y", "Update Z").

### 5. Push to your fork

```bash
git push -u origin my-new-skill
```

### 6. Open a pull request

- Go to your fork on github.com.
- Click **Compare & pull request**.
- Title: a short summary of the change.
- Description: what you changed, why, and any testing notes.
- Submit.

The maintainer will review, possibly ask for changes, and merge.

## Adding a new skill — step by step

1. **Copy the template:** duplicate `skills/_template/` to `skills/<your-skill-name>/`. Use a lowercase, dash-separated folder name (e.g. `meeting-notes`).
2. **Fill in `skill.yaml`:** update `name`, `description`, `version`, `tags`, etc. The folder name and the `name:` field must match.
3. **Write `SKILL.md`:** instructions Claude/Cowork should follow when invoking the skill. Use the template's section structure.
4. **Add any helper files** (templates, data, prompts) the skill needs.
5. **(Optional) Test locally:** from the repo root, run
   ```bash
   bash scripts/build-skills.sh
   python scripts/update-readme-table.py
   ```
   to confirm your skill packages cleanly and shows up in the README table.
6. **Open a pull request.** When it merges, CI will:
   - Build a `.zip` of your skill folder
   - Publish it as a [GitHub Release asset](https://github.com/jiriforman/skills/releases/latest) — downloadable at `https://github.com/jiriforman/skills/releases/latest/download/<your-skill-name>.zip`
   - Refresh the skills table in the README

### `skill.yaml` schema

| Field | Required | Description |
|---|---|---|
| `name` | ✅ | Machine-readable name; must match the folder. Lowercase, dash-separated. |
| `display_name` |  | Human-readable name shown in the README table. |
| `description` | ✅ | One-sentence summary. Shown in the README and the catalog site. |
| `version` | ✅ | Semantic version (`MAJOR.MINOR.PATCH`). Bump on meaningful changes. |
| `tags` |  | List of tag strings (used for catalog filtering). |
| `install_method` | ✅ | `zip` (helper files; must install from `.zip`) or `paste` (markdown-only). |
| `requires` |  | List of other skill names this one depends on. |
| `author` |  | GitHub handle of the original author. |

### Versioning convention

- **PATCH** (`1.0.0 → 1.0.1`) — wording fixes, clarifications, helper-file tweaks. No behavior change.
- **MINOR** (`1.0.1 → 1.1.0`) — new capabilities added, but existing prompts still work.
- **MAJOR** (`1.1.0 → 2.0.0`) — breaking change. The skill's interface, inputs, or outputs changed in a way that may surprise existing users.

## Style notes

- Prefer plain Markdown; avoid platform-specific formatting.
- Use clear, friendly language — skills should be readable by non-experts.
- Don't include secrets, API keys, or proprietary data in committed files.

## Code of conduct

Be kind, be constructive, assume good faith. Disagreements are fine — disrespect is not.

## Questions?

Open an issue with the **question** label and I'll get back to you.
