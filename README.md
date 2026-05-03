[![Publish Python Package to PyPI](https://github.com/Sahaj001/Script-Manager/actions/workflows/publish.yml/badge.svg)](https://github.com/Sahaj001/Script-Manager/actions/workflows/publish.yml)

# Script-Command-Manager (SCM)
# 🚀 SCM Tool Guide

A streamlined command manager for your terminal workflows.

## Overview

**SCM** is a high-performance CLI tool designed to catalog, manage, and execute complex shell commands through an intuitive fuzzy-finding interface. Built with Python and powered by `fzf`, it eliminates the need to remember arcane syntax or sift through endless history files.

## Features
*   **Fuzzy Search Navigation**: Instant filtering of categories and commands using `fzf`.
*   **Hierarchical Management**: Organize commands into custom categories (e.g., Work, Dev, Personal).
*   **In-App Administration**: Add or delete commands and entire categories directly from the interface.
*   **Shell History Integration**: Commands executed via SCM can be injected into your shell history for easy access later.
*   **Mac-Optimized Core**: Robust file I/O designed to handle macOS-specific shell environments and `sed/grep` variations.

---

## Installation

### Prerequisites
1.  **Python**: 3.6 or higher.
2.  **fzf**: Must be installed on your system.
    ```bash
    brew install fzf
    ```

### Local Setup
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Sahaj001/Script-Manager.git](https://github.com/Sahaj001/Script-Manager.git)
    cd Script-Manager
    ```
2.  Install in editable mode:
    ```bash
    pip install -e .
    ```

---

## Configuration

To enable command execution and history injection, add the following wrapper to your `~/.zshrc` or `~/.bashrc`:
```bash
### SCM START ###
rscm() {
    local result=$(scm)
    if [[ -n "$result" ]]; then
        eval " $result"
    fi
}
alias s='rscm'
### SCM END ###
```


---
### 🚀 Usage
> **Note**
> Simply type `s` or `run_scm` in your terminal to launch the interactive menu.


---

## 🛠 Features & Navigation

*   **Select a Category:** Use the **arrow keys** to navigate or **start typing** to filter through your existing groups.
*   **Execute:** Choose a specific command and hit `Enter` to run it directly in your current shell.
*   **Management:**
    *   `[+ Add New Category]` — Create a new group for your commands.
    *   `[+ Add Command to...]` — Expand your library within a specific category.
    *   `[-] Delete` — Prune old or unused commands and groups.

---


## 🤝 Contributing

Contributions make the terminal better for everyone! 

1.  **Fork** the repository.
2.  **Submit** a pull request with your improvements.
3.  *For major changes:* Please **open an issue** first to discuss your ideas so we can stay aligned on the project goals.

License
Apache License 2.0

