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

## Adding a new skill — checklist

When proposing a new skill, please include:

- [ ] A `SKILL.md` (or equivalent) with clear instructions for Claude/Cowork.
- [ ] A short description (1–2 sentences) of what the skill does.
- [ ] Tags/category (e.g. Productivity, Finance, Communication).
- [ ] Any helper files the skill depends on.
- [ ] Notes on installation (especially if the skill must be installed from a `.zip`).
- [ ] (Optional) An example prompt or expected output, so reviewers can try it.

## Style notes

- Prefer plain Markdown; avoid platform-specific formatting.
- Use clear, friendly language — skills should be readable by non-experts.
- Don't include secrets, API keys, or proprietary data in committed files.

## Code of conduct

Be kind, be constructive, assume good faith. Disagreements are fine — disrespect is not.

## Questions?

Open an issue with the **question** label and I'll get back to you.
