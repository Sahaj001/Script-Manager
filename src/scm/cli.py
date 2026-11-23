"""CLI implementation for Script Command Manager (SCM)."""
from __future__ import annotations

import os
import subprocess
import sys
from typing import List


CONFIG_FILE = os.path.expanduser("~/.work_commands")


def load_commands() -> List[List[str]]:
    """Load commands from the config file."""
    if not os.path.exists(CONFIG_FILE):
        return []
    commands: List[List[str]] = []
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            commands.append(line.split("|", 2))
    return commands


def save_commands(commands: List[List[str]]) -> None:
    """Save commands to the config file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for cmd in commands:
            f.write("|".join(cmd) + "\n")


def run_fzf(options: List[str], header: str) -> str | None:
    """Run fuzzy finder and return the selected option."""
    input_str = "\n".join(options)
    try:
        with subprocess.Popen(
            ["fzf", "--height", "40%", "--reverse", "--header", header],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        ) as process:
            stdout, _ = process.communicate(input=input_str)
            return stdout.strip() if stdout else None
    except FileNotFoundError:
        print("Error: 'fzf' binary not found. Please install it via brew/apt.")
        return None
    except subprocess.SubprocessError:
        return None


def prompt_user(msg: str) -> str:
    """Prompt the user for input."""
    sys.stderr.write(f"{msg}: ")
    sys.stderr.flush()
    return sys.stdin.readline().strip()


def add_new_command(commands: List[List[str]], category: str | None = None) -> None:
    """Handle adding a new command via interactive prompts."""
    target_cat = category or prompt_user("Enter Category Name")
    name = prompt_user("Enter Display Name")
    cmd = prompt_user("Enter Bash Command")

    if target_cat and name and cmd:
        commands.append([target_cat, name, cmd])
        save_commands(commands)
        print(f"echo '✅ Added to {target_cat}'")


def delete_logic(commands: List[List[str]], category: str | None = None) -> None:
    """Handle deletion of a whole category or a single command."""
    if category is None:
        categories = sorted({c[0] for c in commands})
        if not categories:
            print("echo 'No categories to delete!'")
            return

        cat_to_wipe = run_fzf(categories, "SELECT CATEGORY TO WIPE ENTIRELY")
        if cat_to_wipe:
            conf = prompt_user(f"Delete ALL commands in [{cat_to_wipe}]? (y/n)")
            if conf and conf.lower() == "y":
                updated_commands = [c for c in commands if c[0] != cat_to_wipe]
                save_commands(updated_commands)
                print(f"echo '❌ Category [{cat_to_wipe}] deleted!'")
        return

    sub_cmds = [c for c in commands if c[0] == category]
    cat_raw = [f"{c[1]} | {c[2]}" for c in sub_cmds]

    to_delete_display = run_fzf(cat_raw, f"SELECT COMMAND TO DELETE FROM {category}")

    if to_delete_display:
        parts = [x.strip() for x in to_delete_display.split("|", 1)]
        if len(parts) == 2:
            d_name, d_cmd = parts[0], parts[1]
            updated_commands = [
                c
                for c in commands
                if not (c[0] == category and c[1] == d_name and c[2] == d_cmd)
            ]
            save_commands(updated_commands)
            print(f"echo '❌ Deleted [{d_name}] from {category}'")


def main() -> None:
    """Main entry point for the SCM CLI."""
    while True:
        commands = load_commands()
        categories = sorted({c[0] for c in commands})

        cat_options = categories + ["[+ Add New Category]", "[- Delete Category]"]
        category = run_fzf(cat_options, "Select Category (Esc to Exit)")

        if not category:
            sys.exit(0)

        if category == "[+ Add New Category]":
            add_new_command(commands)
            return

        if category == "[- Delete Category]":
            delete_logic(commands)
            return

        sub_cmds = [c for c in commands if c[0] == category]
        cmd_options = [f"{c[1]}|{c[2]}" for c in sub_cmds]
        cmd_options += [
            f"[+ Add Command to {category}]",
            f"[- Delete Command from {category}]",
        ]

        selection = run_fzf(cmd_options, f"Commands in {category}")

        if not selection:
            continue

        if selection == f"[+ Add Command to {category}]":
            add_new_command(commands, category)
            return

        if selection == f"[- Delete Command from {category}]":
            delete_logic(commands, category)
            return

        print(selection.split("|", 1)[-1])
        break


if __name__ == "__main__":
    main()
