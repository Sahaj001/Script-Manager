# main.py
import subprocess
import os
import sys

CONFIG_FILE = os.path.expanduser("~/.work_commands")


def load_commands():
    """Loods commadns"""
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        # Filter out empty lines and ensure 3 parts per line
        return [line.strip().split("|") for line in f if line.strip() and "|" in line]


def save_commands(commands):
    """Save commands"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for cmd in commands:
            f.write("|".join(cmd) + "\n")


def run_fzf(options, header):
    """Run fuzzy finder"""
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


def prompt_user(msg):
    """Prompt to user"""
    sys.stderr.write(f"{msg}: ")
    sys.stderr.flush()
    return sys.stdin.readline().strip()


def add_new_command(commands, category=None):
    """Handles the UI and logic for adding a new command."""
    target_cat = category or prompt_user("Enter Category Name")
    name = prompt_user("Enter Display Name")
    cmd = prompt_user("Enter Bash Command")

    if target_cat and name and cmd:
        commands.append([target_cat, name, cmd])
        save_commands(commands)
        print(f"echo '✅ Added to {target_cat}'")


def delete_category(commands):
    """Handles wiping an entire category."""
    categories = sorted(list(set(c[0] for c in commands)))
    if not categories:
        print("echo 'No categories to delete!'")
        return commands

    cat_to_wipe = run_fzf(categories, "SELECT CATEGORY TO WIPE ENTIRELY")
    if cat_to_wipe:
        conf = prompt_user(f"Delete ALL commands in [{cat_to_wipe}]? (y/n)")
        if conf.lower() == "y":
            commands = [c for c in commands if c[0] != cat_to_wipe]
            save_commands(commands)
            print(f"echo '❌ Category [{cat_to_wipe}] deleted!'")
    return commands


def main():
    """Main function - Orchestrates the menu navigation."""
    while True:
        commands = load_commands()
        categories = sorted(list(set(c[0] for c in commands)))

        # 1. CATEGORY LEVEL
        cat_options = categories + ["[+ Add New Category]", "[- Delete Category]"]
        category = run_fzf(cat_options, "Select Category (Esc to Exit)")

        if not category:
            sys.exit(0)

        if category == "[+ Add New Category]":
            add_new_command(commands)
            return

        if category == "[- Delete Category]":
            delete_category(commands)
            return

        # 2. COMMAND LEVEL
        sub_cmds = [c for c in commands if c[0] == category]
        cmd_options = [f"{c[1]}|{c[2]}" for c in sub_cmds]
        cmd_options += [f"[+ Add Command to {category}]"]

        selection = run_fzf(cmd_options, f"Commands in {category}")

        if not selection:
            continue

        if selection == f"[+ Add Command to {category}]":
            add_new_command(commands, category)
            return

        # 3. EXECUTE
        print(selection.split("|", maxsplit=-1)[-1])
        break
