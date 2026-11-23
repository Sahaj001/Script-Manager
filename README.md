# Script Command Manager (SCM)

[![Publish Python Package to PyPI](https://github.com/Sahaj001/Script-Manager/actions/workflows/publish.yml/badge.svg)](https://github.com/Sahaj001/Script-Manager/actions/workflows/publish.yml)
[![Pylint](https://github.com/Sahaj001/Script-Manager/actions/workflows/pylint.yml/badge.svg)](https://github.com/Sahaj001/Script-Manager/actions/workflows/pylint.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A fast, terminal-first command manager for organizing and running shell commands with `fzf`.

## Overview

SCM helps you store frequently used shell commands by category and run them through an interactive fuzzy-search menu. It is designed for developers who want quick access to repeatable workflows without cluttering shell history manually.

## Features

- Fuzzy search with `fzf` for categories and commands
- Hierarchical organization by category
- In-app add/delete flows for commands and categories
- Lightweight local storage in `~/.work_commands`
- Simple shell integration for execution

## Requirements

- Python 3.6+
- [`fzf`](https://github.com/junegunn/fzf)

Install `fzf` on macOS:

```bash
brew install fzf
```

## Installation

### From source (local development)

```bash
git clone https://github.com/Sahaj001/Script-Manager.git
cd Script-Manager
pip install -e .
```

## Shell Setup

Add the following function/alias to your `~/.zshrc` or `~/.bashrc`:

```bash
scm_run() {
  local result
  result="$(scm)"
  if [[ -n "$result" ]]; then
    eval "$result"
  fi
}

alias s='scm_run'
```

Reload your shell config:

```bash
source ~/.zshrc   # or source ~/.bashrc
```

## Usage

Run:

```bash
s
```

Navigation:

- Use arrow keys or type to filter
- Press `Enter` to execute a selected command
- Use `[+ Add New Category]` to create categories
- Use `[+ Add Command to ...]` to add commands
- Use delete options to remove commands/categories

## Data Storage

Commands are stored locally at:

```text
~/.work_commands
```

Format per line:

```text
Category|Display Name|Shell Command
```

## Development

Install in editable mode:

```bash
pip install -e .
```

Run lint:

```bash
pylint $(git ls-files '*.py') --disable=C0114,C0115,C0116,R1710,R0912,R1705
```

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

For major changes, open an issue first to discuss what you would like to change.

## License

Licensed under the [Apache License 2.0](LICENSE).


