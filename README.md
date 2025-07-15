# Python Shell

A simple shell implementation built in Python. This project provides a minimal command-line interface with several built-in commands and the ability to run executables from your system's PATH.

## Features

- **Command execution:** Run any executable available in your system's PATH.
- **Tab completion:** Autocomplete for built-in and PATH commands using the Tab key.
- **Command history:** View and recall previous commands with the `history` command.
- **Change directory:** Use `cd <directory>` to change the current working directory.
- **Print working directory:** Use `pwd` to display the current directory.
- **Echo:** Use `echo <text>` to print text to the shell.
- **Type:** Use `type <command>` to check if a command is a shell builtin or an external executable.
- **Exit:** Use `exit` to leave the shell.
- **Output redirection:** Supports basic output redirection using `>` or `1>`.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/meenakship3/shell-python
   cd shell-python
   ```
2. Run the shell:
   ```bash
   python app/main.py
   ```

## Libraries Used

- `os` — For interacting with the operating system, directories, and environment variables.
- `sys` — For system-specific parameters and functions.
- `subprocess` — For running external commands and programs.
- `pathlib` — For object-oriented filesystem paths.
- `shlex` — For parsing shell-like syntax.
- `readline` — For command line editing and history features.
- `rlcompleter` — For tab completion support in the shell.

All libraries used are part of the Python standard library; no third-party dependencies are required.

## Notes
- The shell assumes a UNIX-like environment for PATH handling.
- Output redirection is handled via the system shell for lines containing `>` or `1>`.