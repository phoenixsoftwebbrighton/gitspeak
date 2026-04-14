# 🛠️ Tool: GitSpeak
> A plain English Git command builder — type a keyword, fill in the blank, done.

---

## The Problem It Solves

Git commands are long, hard to remember, and unforgiving if you get them wrong.
Most people copy-paste from Google every single time.
For neurodivergent users, remembering exact syntax is a genuine barrier.

**GitSpeak removes the barrier** — you only ever type what's unique to your situation.
The rest is handled for you.

---

## How It Works

```
User types:   commit
GitSpeak:     What's your commit message?
User types:   add unknown error submission feature
GitSpeak:     Running: git commit -m "add unknown error submission feature"  ✅
```

```
User types:   push
GitSpeak:     Running: git push origin main  ✅
```

```
User types:   branch
GitSpeak:     What do you want to call the new branch?
User types:   feature/web-interface
GitSpeak:     Running: git checkout -b feature/web-interface  ✅
```

---

## Planned Keywords

| Keyword | What it does | Asks for |
|---|---|---|
| `commit` | Stages and commits everything | Commit message |
| `push` | Pushes to origin main | Nothing — just runs |
| `pull` | Pulls latest from origin | Nothing — just runs |
| `status` | Shows what's changed | Nothing — just runs |
| `branch` | Creates a new branch | Branch name |
| `switch` | Switches to an existing branch | Branch name |
| `undo` | Undoes the last commit safely | Nothing — just runs |
| `log` | Shows recent commits in plain English | Nothing — just runs |
| `save` | Stages + commits + pushes in one go | Commit message |
| `init` | Initialises a new repo | Nothing — just runs |
| `remote` | Sets the remote URL | The URL |
| `help` | Lists all available keywords | Nothing — just runs |

---

## Design Rules (same as all our tools)

- Max 1 question per command — never ask more than one thing
- Plain English prompts — no jargon
- Always show the full command before running it so the user can learn
- If something goes wrong, translate the error using Decipher's logic
- Works standalone in Terminal — no dependencies on anything else

---

## Connection to Decipher

If a Git command fails, GitSpeak passes the error straight to Decipher's translation engine.
The user never sees a raw error message — they see a plain English explanation instead.

This is the first example of two tools working together.

---

## Future ideas

- `save` keyword — add + commit + push in one go
- Suggested commit messages based on what files changed
- Undo history — "what did I just do?" shows recent commands in plain English

---

*Part of the neurodivergent developer toolkit — same mission, different tool.*
