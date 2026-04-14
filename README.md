# 🗣️ GitSpeak

---

> **"Git without the syntax. Just say what you want to do."**

Git is powerful. Git is also full of commands that are easy to forget, easy to get wrong, and completely unforgiving when you miss a step. GitSpeak fixes that — type one word, answer one question, and it handles the rest.

---

## Why it exists

The most common Git mistake isn't understanding Git — it's forgetting one step in the sequence. You commit but forget to push. You push but forget to stage. You stage but forget to commit. Each one fails silently or with an error that doesn't tell you what you actually missed.

GitSpeak collapses the whole workflow into one word.

---

## How to run it

```bash
python3 gitspeak.py
```

Or if you've added the alias (recommended):

```bash
gs
```

To add the alias permanently:

```bash
echo 'alias gs="python3 ~/Projects/tools/gitspeak/gitspeak.py"' >> ~/.zshrc && source ~/.zshrc
```

---

## Commands

| Type this | What it does | Asks you for |
|---|---|---|
| `save` | Stage + commit + push — all in one go | Your commit message |
| `commit` | Stage and commit without pushing | Your commit message |
| `push` | Push to origin main | Nothing |
| `pull` | Pull latest from origin | Nothing |
| `status` | Show what's changed in plain English | Nothing |
| `log` | Show recent commits in plain English | Nothing |
| `branch` | Create a new branch | Branch name |
| `switch` | Switch to a different branch | Branch name |
| `undo` | Undo the last commit safely (files stay) | Confirmation |
| `init` | Start a new git repo | Nothing |
| `remote` | Set or update the remote URL | The URL |
| `help` | Show all commands | Nothing |
| `exit` | Quit GitSpeak | Nothing |

---

## The star of the show — `save`

This is the command that replaces three separate steps most people forget to do in the right order:

```
Without GitSpeak:                With GitSpeak:

git add -A                       gs
git commit -m "your message"     save
git push origin main             add the readme and docs
                                 ✅ Done
```

One word. One question. Everything saved and pushed.

---

## What happens when something goes wrong?

If a command fails, GitSpeak shows you the error in plain English and suggests pasting it into Decipher for a full translation and fix steps.

GitSpeak and Decipher are designed to work together — GitSpeak runs your commands, Decipher explains when they break.

---

## Project structure

```
gitspeak/
├── gitspeak.py       ← the main app
├── GITSPEAK-IDEA.md  ← original design notes
└── README.md         ← you are here
```

---

## Roadmap

- [ ] Auto-detect remote URL on startup — show where commands will push to
- [ ] Warn if no remote is set before attempting to push
- [ ] Suggested commit messages based on what files changed
- [ ] Plain English `log` output — "3 days ago you added the error database"
- [ ] Integration with Decipher — errors auto-translated without copy-pasting

---

## Part of the neurodivergent developer toolkit

GitSpeak is part of a wider project to build tech tools for neurodivergent people. Finally, built by someone with lived experience.

> **"Built for the developers who kept being told the problem was them. It wasn't."**

---

*Built by Ash Baguley — Brighton, UK*
