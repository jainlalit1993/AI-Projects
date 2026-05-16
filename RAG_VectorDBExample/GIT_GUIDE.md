# Git Guide — Installation, Workflow & Strategies

A practical reference for using Git effectively, from first install to team collaboration strategies.

---

## 1. Installation

### Windows

1. Download the installer from [git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer — the defaults are fine for most users
3. During setup, select **"Git from the command line and also from 3rd-party software"**
4. Verify the install:

```bash
git --version
```

> **Recommended extras:**
> - [GitHub Desktop](https://desktop.github.com) — a GUI if you prefer clicking over typing
> - [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) — handles GitHub login (included in the Git for Windows installer)

---

### macOS

**Option A — via Xcode Command Line Tools (easiest):**
```bash
xcode-select --install
```

**Option B — via Homebrew (recommended for developers):**
```bash
brew install git
```

Verify:
```bash
git --version
```

---

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install git
```

**Fedora / RHEL:**
```bash
sudo dnf install git
```

Verify:
```bash
git --version
```

---

## 2. First-Time Configuration

Run these once after installation. Git stamps every commit with this identity.

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"   # uses VS Code as default editor
git config --global init.defaultBranch main
```

Check your config:
```bash
git config --list
```

---

## 3. Core Concepts (Quick Reference)

| Term | What it means |
|---|---|
| **Repository (repo)** | A folder tracked by Git |
| **Working directory** | The files you are editing right now |
| **Staging area (index)** | A holding area — files you have `git add`-ed but not committed yet |
| **Commit** | A permanent snapshot of your staged changes |
| **Branch** | A parallel line of development |
| **Remote** | A copy of the repo hosted elsewhere (GitHub, GitLab, etc.) |
| **HEAD** | A pointer to the commit you are currently on |

---

## 4. The Daily Git Workflow

These 5 commands cover 90% of everyday use.

```bash
# 1. Pull the latest changes before you start
git pull

# 2. Make your changes, then check what changed
git status
git diff

# 3. Stage the files you want to commit
git add filename.py         # one file
git add .                   # everything in the current folder

# 4. Commit with a meaningful message
git commit -m "Add cosine similarity comparison to script 01"

# 5. Push your commits to the remote
git push
```

---

## 5. Branching Strategies

### Strategy A — Trunk-Based Development (recommended for small teams / solo projects)

Everyone commits directly to `main` (or merges short-lived branches quickly).

```
main  ──●──●──●──●──●──►
```

**When to use it:** Solo projects, small teams (2–4 people), fast-moving codebases.

**Rules:**
- Keep `main` always deployable
- Commits should be small and frequent
- Use feature flags for incomplete work instead of long-lived branches

```bash
# Work directly on main
git checkout main
git pull
# ... make small change ...
git add .
git commit -m "Fix: handle empty query in script 05"
git push
```

---

### Strategy B — Feature Branch Workflow (recommended for most teams)

Each new feature or fix gets its own branch. Changes merge back to `main` via a Pull Request.

```
main     ──●────────────────●──►
              \            /
feature/login  ●──●──●──●
```

**When to use it:** Teams of any size, when you want code review before merging.

```bash
# 1. Create a branch for your work
git checkout -b feature/add-metadata-filter

# 2. Work, commit, push the branch
git add .
git commit -m "Add category filter to query function"
git push -u origin feature/add-metadata-filter

# 3. Open a Pull Request on GitHub, get it reviewed, then merge

# 4. After merge, clean up
git checkout main
git pull
git branch -d feature/add-metadata-filter
```

**Branch naming conventions:**
```
feature/short-description    ← new functionality
fix/bug-description          ← bug fixes
docs/what-you-updated        ← documentation only
refactor/what-changed        ← restructuring without behaviour change
chore/task-description       ← tooling, dependencies, config
```

---

### Strategy C — Git Flow (for projects with scheduled releases)

Uses two permanent branches (`main` = production, `develop` = integration) plus supporting branches.

```
main     ──●────────────────────●──►  (production only)
              \                /
develop   ─────●──●──●──●──●──────►  (integration)
                  \      /
feature/x          ●──●
```

**When to use it:** Products with versioned releases, mobile apps, libraries with semantic versioning.

```bash
# Feature starts from develop
git checkout develop
git checkout -b feature/add-new-embedding-model

# When done, merge back to develop
git checkout develop
git merge feature/add-new-embedding-model

# Release: cut a release branch from develop
git checkout -b release/1.2.0
# fix release bugs here, then merge to BOTH main AND develop
git checkout main
git merge release/1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"
```

> **Tip:** For most projects, Feature Branch Workflow (Strategy B) is simpler and sufficient. Only adopt Git Flow if you genuinely need multiple concurrent versions in production.

---

## 6. Working with GitHub

### Clone an existing repo
```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

### Link a local repo to GitHub
```bash
git remote add origin https://github.com/username/repo-name.git
git branch -M main
git push -u origin main
```

### Fork → Contribute → Pull Request (open-source workflow)
```bash
# 1. Fork the repo on GitHub (click "Fork" button)
# 2. Clone YOUR fork
git clone https://github.com/your-username/repo-name.git

# 3. Add the original repo as "upstream"
git remote add upstream https://github.com/original-owner/repo-name.git

# 4. Keep your fork up to date
git fetch upstream
git merge upstream/main

# 5. Create a branch, make changes, push, then open a PR on GitHub
```

---

## 7. Undoing Mistakes

| Situation | Command |
|---|---|
| Undo unstaged changes to a file | `git restore filename.py` |
| Unstage a file you added by mistake | `git restore --staged filename.py` |
| Undo the last commit (keep changes) | `git reset --soft HEAD~1` |
| Undo the last commit (discard changes) | `git reset --hard HEAD~1` ⚠️ |
| Revert a commit (safe, creates new commit) | `git revert <commit-hash>` |
| Stash work-in-progress temporarily | `git stash` / `git stash pop` |

> ⚠️ `--hard` is destructive — your changes are gone. Prefer `--soft` when in doubt.

---

## 8. Inspecting History

```bash
git log                        # full history
git log --oneline              # compact one-line view
git log --oneline --graph      # visual branch tree
git log --author="Your Name"   # filter by author
git diff HEAD~1                # diff against previous commit
git show <commit-hash>         # show a specific commit
git blame filename.py          # see who wrote each line
```

---

## 9. What to Never Commit

Add these to `.gitignore` before your first commit:

```
# Secrets and credentials
.env
*.pem
secrets.json

# Dependencies (can be reinstalled)
node_modules/
venv/
__pycache__/

# Generated files
*.pyc
dist/
build/

# Large binary / data files
*.bin
*.sqlite3
chroma_db/
```

**Rule of thumb:** If it contains a password, can be regenerated, or is larger than a few MB — it should not be in Git.

---

## 10. Commit Message Best Practices

A good commit message answers: *"What does this change do, and why?"*

**Format:**
```
<type>: <short summary in present tense, max 72 chars>

<optional body — explain WHY, not WHAT, if needed>
```

**Examples:**
```bash
git commit -m "feat: add metadata filtering to vector search"
git commit -m "fix: handle empty query string in script 05"
git commit -m "docs: add installation steps to README"
git commit -m "refactor: extract embedding helper into utils module"
git commit -m "chore: update chromadb to 0.5.0"
```

**Types:** `feat` | `fix` | `docs` | `refactor` | `test` | `chore`

---

## 11. Quick Command Cheatsheet

```bash
# Setup
git init                          # initialise a new repo
git clone <url>                   # clone a remote repo

# Daily workflow
git status                        # see what changed
git diff                          # see exact changes
git add <file>                    # stage a file
git add .                         # stage everything
git commit -m "message"           # commit staged changes
git push                          # push to remote
git pull                          # fetch + merge from remote

# Branches
git branch                        # list branches
git checkout -b <branch-name>     # create + switch to branch
git checkout <branch-name>        # switch to existing branch
git merge <branch-name>           # merge branch into current
git branch -d <branch-name>       # delete branch (after merge)

# Remote
git remote -v                     # list remotes
git remote add origin <url>       # link to remote
git push -u origin <branch>       # push + track remote branch

# History
git log --oneline                 # compact history
git show <hash>                   # inspect a commit
git blame <file>                  # see who wrote each line
```

---

## Further Reading

- [Pro Git book (free)](https://git-scm.com/book/en/v2) — the definitive Git reference
- [GitHub Skills](https://skills.github.com) — interactive hands-on courses
- [Conventional Commits](https://www.conventionalcommits.org) — a standard for commit message format
- [Oh Shit, Git!](https://ohshitgit.com) — plain-English fixes for common mistakes
