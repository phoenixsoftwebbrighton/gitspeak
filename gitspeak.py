#!/usr/bin/env python3
import subprocess
import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from datetime import datetime

console = Console()

# ── find Decipher's database ──────────────────────────────────────────────────

TOOLS_DIR = Path(__file__).parent.parent
DECIPHER_ERRORS = TOOLS_DIR / "decipher" / "errors.json"
DECIPHER_UNKNOWN = TOOLS_DIR / "decipher" / "unknown_errors.json"

def load_decipher_db():
    """Load Decipher's error database if it exists"""
    if DECIPHER_ERRORS.exists():
        with open(DECIPHER_ERRORS, 'r') as f:
            return json.load(f)
    return []

def save_to_decipher_unknown(error_text, context, tool="Git"):
    """Submit an unknown error to Decipher's community queue"""
    if not DECIPHER_UNKNOWN.exists():
        return False
    with open(DECIPHER_UNKNOWN, 'r') as f:
        unknown = json.load(f)
    entry = {
        "id": len(unknown) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "error": error_text,
        "context": context,
        "tool": tool,
        "source": "GitSpeak",
        "status": "pending"
    }
    unknown.append(entry)
    with open(DECIPHER_UNKNOWN, 'w') as f:
        json.dump(unknown, f, indent=2)
    return len(unknown)

def decipher_lookup(error_text):
    """Search Decipher's database for a matching error"""
    db = load_decipher_db()
    search = error_text.lower()
    for entry in db:
        if entry['robot_error'].lower() in search:
            return entry
    return None

# ── helpers ──────────────────────────────────────────────────────────────────

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output

def show_success(command, output=""):
    msg = f"[bold]Command run:[/bold] [dim]{command}[/dim]"
    if output:
        msg += f"\n\n{output}"
    console.print(Panel(msg, title="[bold green]✅ Done[/bold green]", border_style="green"))

def handle_error(error_text, context):
    """
    1. Search Decipher's database automatically
    2. Show translation if found
    3. Offer to submit to community database if not
    """
    match = decipher_lookup(error_text)

    if match:
        steps = "\n".join([f"  {i+1}. {s}" for i, s in enumerate(match['fix_steps'])])
        console.print(Panel(
            f"[bold]What this means:[/bold]\n  {match['human_truth']}\n\n"
            f"[bold]How to fix it:[/bold]\n{steps}\n\n"
            f"[dim]Translation provided by Decipher[/dim]",
            title="[bold cyan]🔍 Decipher knows this one[/bold cyan]",
            border_style="cyan"
        ))
    else:
        console.print(Panel(
            f"[bold]What went wrong:[/bold]\n{error_text}\n\n"
            f"[bold]Context:[/bold] {context}",
            title="[bold red]❌ Something went wrong[/bold red]",
            border_style="red"
        ))

        if DECIPHER_UNKNOWN.exists():
            console.print(
                "\n[yellow]Decipher doesn't know this error yet.[/yellow]\n"
                "[dim]Would you like to add it to the community database so it helps the next person?[/dim]"
            )
            answer = input("\n  Submit to Decipher? (yes/no): ").strip().lower()

            if answer in ["yes", "y"]:
                entry_number = save_to_decipher_unknown(error_text, context)
                if entry_number:
                    console.print(Panel(
                        f"Saved as entry #{entry_number} in Decipher's queue. ✅\n\n"
                        "Every submission makes the toolkit smarter for the next person.\n"
                        "Thank you for contributing to the community.",
                        title="[bold green]📬 Submitted to Decipher[/bold green]",
                        border_style="green"
                    ))
            else:
                console.print("[dim]No problem — skipped.[/dim]\n")

def ask(question):
    console.print(f"\n[cyan]→[/cyan] {question}")
    return input("  ").strip()

# ── startup check ─────────────────────────────────────────────────────────────

def startup_check():
    ok, _ = run("git rev-parse --is-inside-work-tree")
    if not ok:
        console.print(Panel(
            "This folder isn't a git repo yet.\n\n"
            "Type [bold]init[/bold] to start one, or navigate to a project folder first.",
            title="[bold yellow]⚠️  No git repo found[/bold yellow]",
            border_style="yellow"
        ))
        return

    ok, remote_url = run("git remote get-url origin")

    if ok and remote_url:
        ok2, branch = run("git branch --show-current")
        branch = branch.strip() if ok2 else "main"
        ok3, status = run("git status --short")
        changes = len(status.strip().split("\n")) if status.strip() else 0
        change_text = f"{changes} unsaved change(s)" if changes else "nothing to save"

        decipher_status = "✅ connected" if DECIPHER_ERRORS.exists() else "⚠️  not found"

        console.print(Panel(
            f"[bold]Repo:[/bold]     {remote_url}\n"
            f"[bold]Branch:[/bold]   {branch}\n"
            f"[bold]Status:[/bold]   {change_text}\n"
            f"[bold]Decipher:[/bold] {decipher_status}\n\n"
            "[dim]All push/pull commands will use the repo above.[/dim]",
            title="[bold cyan]📡 Connected[/bold cyan]",
            border_style="cyan"
        ))
    else:
        console.print(Panel(
            "This repo has no remote URL set — if you try to push, it will fail.\n\n"
            "Type [bold]remote[/bold] to set one now, or carry on if you're working locally.",
            title="[bold yellow]⚠️  No remote URL found[/bold yellow]",
            border_style="yellow"
        ))

# ── commands ─────────────────────────────────────────────────────────────────

def cmd_save():
    message = ask("What did you work on? (this becomes your commit message)")
    if not message:
        console.print("[yellow]No message entered — cancelled.[/yellow]")
        return

    safe_message = message.replace("'", "")
    commit_cmd = f"git add -A && git commit -m '{safe_message}'"
    push_cmd = "git push origin main"

    console.print(f"\n[dim]Running: {commit_cmd} && {push_cmd}[/dim]\n")

    ok, out = run(commit_cmd)
    if not ok:
        # If nothing to commit, still try to push in case there are unpushed commits
        if "nothing to commit" in out:
            console.print("[dim]Nothing new to commit — checking if there's anything to push...[/dim]\n")
        else:
            handle_error(out, f"trying to commit: {safe_message}")
            return

    ok, out = run(push_cmd)

    # If remote has commits we don't have locally, pull first then push
    if not ok and ("fetch first" in out or "rejected" in out):
        console.print("[dim]Remote has new changes — pulling first...[/dim]\n")
        ok, pull_out = run("git pull --rebase origin main")
        if not ok:
            handle_error(pull_out, "trying to pull before pushing")
            return
        ok, out = run(push_cmd)

    if ok:
        show_success(f"{commit_cmd} && {push_cmd}", "Everything saved and pushed. ✅")
    else:
        handle_error(out, "trying to push to origin main")

def cmd_commit():
    message = ask("What did you work on? (this becomes your commit message)")
    if not message:
        console.print("[yellow]No message entered — cancelled.[/yellow]")
        return

    safe_message = message.replace("'", "")
    command = f"git add -A && git commit -m '{safe_message}'"
    ok, out = run(command)
    if ok:
        show_success(command, out)
    else:
        handle_error(out, f"trying to commit: {safe_message}")

def cmd_push():
    command = "git push origin main"
    console.print(f"\n[dim]Running: {command}[/dim]\n")
    ok, out = run(command)
    if ok:
        show_success(command, out)
    else:
        handle_error(out, "trying to push to origin main")

def cmd_pull():
    # --rebase keeps history clean and handles divergent branches automatically
    command = "git pull --rebase origin main"
    console.print(f"\n[dim]Running: {command}[/dim]\n")
    ok, out = run(command)
    if ok:
        show_success(command, out)
    else:
        handle_error(out, "trying to pull from origin main")

def cmd_status():
    ok, out = run("git status")
    if not out:
        console.print(Panel("Nothing has changed.", title="[cyan]Status[/cyan]", border_style="cyan"))
        return

    lines = out.split("\n")
    changed, untracked, staged = [], [], []

    for line in lines:
        if "modified:" in line:
            changed.append(line.strip().replace("modified:", "✏️  Changed:"))
        elif "new file:" in line:
            staged.append(line.strip().replace("new file:", "✅ New file:"))
        elif line.startswith("\t") and not line.startswith("\tdeleted"):
            untracked.append(f"❓ Not tracked yet: {line.strip()}")

    summary = ""
    if staged:
        summary += "[bold]Ready to commit:[/bold]\n" + "\n".join(staged) + "\n\n"
    if changed:
        summary += "[bold]Changed but not staged:[/bold]\n" + "\n".join(changed) + "\n\n"
    if untracked:
        summary += "[bold]New files not tracked:[/bold]\n" + "\n".join(untracked) + "\n\n"
    if not summary:
        summary = out

    console.print(Panel(summary.strip(), title="[cyan]What's changed[/cyan]", border_style="cyan"))

def cmd_log():
    ok, out = run('git log --oneline -10 --pretty=format:"%h | %ar | %s"')
    if not ok or not out:
        console.print("[yellow]No commits yet, or not a git repo.[/yellow]")
        return
    lines = out.strip().split("\n")
    formatted = "\n".join([f"  {line}" for line in lines])
    console.print(Panel(
        f"[bold]Last {len(lines)} commits:[/bold]\n\n{formatted}",
        title="[cyan]Recent history[/cyan]",
        border_style="cyan"
    ))

def cmd_branch():
    name = ask("What do you want to call the new branch?")
    if not name:
        console.print("[yellow]No name entered — cancelled.[/yellow]")
        return
    name = name.replace(" ", "-").lower()
    command = f"git checkout -b {name}"
    ok, out = run(command)
    if ok:
        show_success(command, f"Now on branch: {name}")
    else:
        handle_error(out, f"trying to create branch: {name}")

def cmd_switch():
    ok, out = run("git branch")
    if out:
        console.print(f"\n[dim]Available branches:[/dim]\n{out}\n")
    name = ask("Which branch do you want to switch to?")
    if not name:
        console.print("[yellow]No name entered — cancelled.[/yellow]")
        return
    command = f"git checkout {name}"
    ok, out = run(command)
    if ok:
        show_success(command, f"Switched to: {name}")
    else:
        handle_error(out, f"trying to switch to branch: {name}")

def cmd_undo():
    ok, out = run('git log --oneline -1 --pretty=format:"%h | %s"')
    if not ok:
        console.print("[yellow]Nothing to undo.[/yellow]")
        return
    console.print(f"\n[dim]Last commit: {out}[/dim]")
    confirm = ask("Undo this commit? Your files won't be deleted. (yes/no)")
    if confirm.lower() not in ["yes", "y"]:
        console.print("[dim]Cancelled.[/dim]")
        return
    command = "git reset --soft HEAD~1"
    ok, out = run(command)
    if ok:
        show_success(command, "Last commit undone. Your files are safe — nothing was deleted.")
    else:
        handle_error(out, "trying to undo last commit")

def cmd_init():
    command = "git init"
    ok, out = run(command)
    if ok:
        show_success(command, out)
    else:
        handle_error(out, "trying to initialise a new repo")

def cmd_remote():
    ok, current = run("git remote get-url origin")
    if ok and current:
        console.print(f"\n[dim]Current remote: {current}[/dim]")
    url = ask("What's the new remote URL? (e.g. http://localhost:3000/username/repo.git)")
    if not url:
        console.print("[yellow]No URL entered — cancelled.[/yellow]")
        return
    ok, out = run("git remote")
    command = f"git remote set-url origin {url}" if "origin" in out else f"git remote add origin {url}"
    ok, out = run(command)
    if ok:
        show_success(command, "Remote URL updated.")
    else:
        handle_error(out, "trying to set remote URL")

def cmd_help():
    help_text = (
        "[bold]save[/bold]      — stage + commit + push all in one go  [dim](most used)[/dim]\n"
        "[bold]commit[/bold]    — stage and commit without pushing\n"
        "[bold]push[/bold]      — push to origin main\n"
        "[bold]pull[/bold]      — pull latest from origin\n"
        "[bold]status[/bold]    — see what's changed\n"
        "[bold]log[/bold]       — see recent commits\n"
        "[bold]branch[/bold]    — create a new branch\n"
        "[bold]switch[/bold]    — switch to a different branch\n"
        "[bold]undo[/bold]      — undo last commit safely\n"
        "[bold]init[/bold]      — start a new git repo\n"
        "[bold]remote[/bold]    — set or update the remote URL\n"
        "[bold]help[/bold]      — show this list\n"
        "[bold]exit[/bold]      — quit GitSpeak"
    )
    console.print(Panel(help_text, title="[cyan]Available commands[/cyan]", border_style="cyan"))

# ── command map ──────────────────────────────────────────────────────────────

COMMANDS = {
    "save": cmd_save, "commit": cmd_commit, "push": cmd_push,
    "pull": cmd_pull, "status": cmd_status, "log": cmd_log,
    "branch": cmd_branch, "switch": cmd_switch, "undo": cmd_undo,
    "init": cmd_init, "remote": cmd_remote, "help": cmd_help,
}

# ── main loop ────────────────────────────────────────────────────────────────

def main():
    console.rule("[bold cyan]GitSpeak // Active[/bold cyan]")
    console.print("[dim]Type a keyword to run a Git command. Type 'help' to see all commands.[/dim]\n")
    startup_check()
    print()

    while True:
        try:
            keyword = input("gitspeak → ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[cyan]Goodbye. 🙂[/cyan]")
            break

        if not keyword:
            continue
        if keyword in ("exit", "quit", "q"):
            console.print("\n[cyan]Goodbye. 🙂[/cyan]")
            break
        if keyword in COMMANDS:
            print()
            COMMANDS[keyword]()
            print()
        else:
            console.print(
                f"\n[yellow]'{keyword}' isn't a GitSpeak command.[/yellow] "
                f"[dim]Type 'help' to see what's available.[/dim]\n"
            )

if __name__ == "__main__":
    main()