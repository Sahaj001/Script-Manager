# main.py
import subprocess
import os
import sys

CONFIG_FILE = os.path.expanduser("~/.work_commands")

def load_commands():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r") as f:
        # Filter out empty lines and ensure 3 parts per line
        return [line.strip().split('|') for line in f if line.strip() and '|' in line]

def save_commands(commands):
    with open(CONFIG_FILE, "w") as f:
        for cmd in commands:
            f.write("|".join(cmd) + "\n")

def run_fzf(options, header):
    input_str = "\n".join(options)
    try:
        process = subprocess.Popen(
            ['fzf', '--height', '40%', '--reverse', '--header', header],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate(input=input_str)
        return stdout.strip()
    except Exception:
        return None

def prompt_user(msg):
    sys.stderr.write(f"{msg}: ")
    sys.stderr.flush()
    return sys.stdin.readline().strip()

def main():
    while True:
        commands = load_commands()
        # Get unique category names
        categories = sorted(list(set(c[0] for c in commands)))
        
        # 1. CATEGORY LEVEL
        cat_options = categories + ["[+ Add New Category]", "[- Delete Category]"]
        category = run_fzf(cat_options, "Select Category (Esc to Exit)")

        if not category:
            sys.exit(0)

        # --- ADD CATEGORY ---
        if category == "[+ Add New Category]":
            cat = prompt_user("Enter Category Name")
            name = prompt_user("Enter Display Name")
            cmd = prompt_user("Enter Bash Command")
            if cat and name and cmd:
                commands.append([cat, name, cmd])
                save_commands(commands)
                print(f"echo '✅ Added to {cat}'")
            return

        # --- DELETE WHOLE CATEGORY ---
        if category == "[- Delete Category]":
            if not categories:
                print("echo 'No categories to delete!'")
                return
                
            # Show ONLY the category names for deletion
            cat_to_wipe = run_fzf(categories, "SELECT CATEGORY TO WIPE ENTIRELY")
            
            if cat_to_wipe:
                conf = prompt_user(f"Delete ALL commands in [{cat_to_wipe}]? (y/n)")
                if conf.lower() == 'y':
                    # Keep only commands that DON'T match this category
                    commands = [c for c in commands if c[0] != cat_to_wipe]
                    save_commands(commands)
                    print(f"echo '❌ Category [{cat_to_wipe}] deleted!'")
            return

        # 2. COMMAND LEVEL
        sub_cmds = [c for c in commands if c[0] == category]
        cmd_options = [f"{c[1]}|{c[2]}" for c in sub_cmds]
        cmd_options += [f"[+ Add Command to {category}]", f"[- Delete Command from {category}]"]
        
        selection = run_fzf(cmd_options, f"Commands in {category} (Esc to Go Back)")

        if not selection:
            continue  # Re-runs the loop, showing the Category menu again

        # --- ADD TO CATEGORY ---
        if selection == f"[+ Add Command to {category}]":
            name = prompt_user("Enter Display Name")
            cmd = prompt_user("Enter Bash Command")
            if name and cmd:
                commands.append([category, name, cmd])
                save_commands(commands)
                print(f"echo '✅ Added to {category}'")
            return

        # --- DELETE SINGLE FROM CATEGORY ---
        if selection == f"[- Delete Command from {category}]":
            # Show specific commands in this category for selective deletion
            cat_raw = [f"{c[1]} | {c[2]}" for c in sub_cmds]
            to_delete_display = run_fzf(cat_raw, f"SELECT COMMAND TO DELETE FROM {category}")
            
            if to_delete_display:
                # Split back to get the original name/cmd for matching
                d_name, d_cmd = [x.strip() for x in to_delete_display.split('|')]
                commands = [c for c in commands if not (c[0] == category and c[1] == d_name and c[2] == d_cmd)]
                save_commands(commands)
                print(f"echo '❌ Deleted from {category}'")
            return

        # 3. EXECUTE
        # Split by '|' and take the last element (the command)
        print(selection.split('|')[-1])
        break
