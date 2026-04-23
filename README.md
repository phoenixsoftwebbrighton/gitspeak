# 🗣️ GitSpeak

> **Git without the syntax.**

Part of the [ADHDeveloper Toolkit](https://github.com/phoenixsoftwebbrighton/adhddeveloper-toolkit) — CLI tools for developers whose brains work differently.

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-cyan.svg)](https://www.python.org/downloads/)

---

## 🤔 What is it?

Git is powerful. Git is also full of commands that are easy to forget, easy to get wrong, and completely unforgiving when you miss a step.

GitSpeak fixes that. Type one word, answer one question, it handles the rest.

---

## ⚡ Quick Start

```bash
# Install dependency
pip install rich

# Run GitSpeak
python3 gitspeak.py
```

Add an alias to your shell for instant access:

```bash
echo 'alias gs="python3 ~/gitspeak/gitspeak.py"' >> ~/.zshrc
source ~/.zshrc

# Now just type:
gs
```

---

## 🛠️ Commands

```
save      — stage + commit + push all in one go  ← most used
commit    — stage and commit without pushing
push      — push to origin main
pull      — pull latest from origin
status    — see what's changed in plain English
log       — see recent commits
branch    — create a new branch
switch    — switch to a different branch
undo      — undo last commit safely
init      — start a new git repo
remote    — set or update the remote URL
help      — show this list
exit      — quit GitSpeak
```

---

## 🔍 Works with Decipher

When something goes wrong, GitSpeak automatically searches [Decipher's](https://github.com/phoenixsoftwebbrighton/decipher) error database and translates the error into plain English — right inside GitSpeak, no copy-pasting required.

Unknown errors get submitted to the community database so they help the next person too.

---

## 🎨 Design Philosophy

- **One word commands** — no flags, no syntax to remember
- **Plain English always** — errors translated automatically
- **Safe by default** — undo is always available
- **Rotating goodbyes** — because tools should be fun to use

---

## 📄 License

MIT — free forever.

---

*Part of the ADHDeveloper Toolkit — made for brains that work differently* 🧠
