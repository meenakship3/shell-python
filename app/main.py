import os
import sys
import subprocess
from pathlib import Path
import shlex
import readline
import rlcompleter


class Shell:
    """A simple shell implementation built using Python."""
    def __init__(self):
        self.running = True
        self.prev_cmds = []

    def get_path_executables(self):
        """Get all executable commands from PATH"""
        executables = set()

        path_env = os.environ.get('PATH', '')

        path_dirs = path_env.split(':')  # assumes UNIX

        for directory in path_dirs:
            if not directory or not os.path.isdir(directory):
                continue

            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)

                    if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                        executables.add(filename)

            except PermissionError:
                continue

        return executables
    def run(self):
        """Main shell loop"""

        def completer(text, state):
            options = ['exit', 'quit', 'history', 'echo', 'cd', 'pwd'] + list(self.get_path_executables())
            matches = [opt + ' ' for opt in options if opt.startswith(text)]
            if state < len(matches):
                return matches[state]
            return None

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")

        while self.running:
            try:
                command = self._get_user_input()
                if command:
                    self._execute_command(command)
            except (EOFError, KeyboardInterrupt):
                print()
                break

    def _get_user_input(self):
        """Get and parse user input"""
        try:
            user_input = input("$ ").strip()
            self.prev_cmds.append(user_input)
            if ">" in user_input or "1>" in user_input: # TODO: rewrite function
                os.system(user_input)
                return
            return shlex.split(user_input) if user_input else []
        except EOFError:
            raise

    def _execute_command(self, command):
        """Execute the given command"""
        cmd_name = command[0]
        match cmd_name:
            case "exit":
                self._handle_exit()
            case "type":
                self._handle_type(command)
            case "echo":
                self._handle_echo(command)
            case "pwd":
                self._handle_pwd()
            case "cd":
                self._handle_cd(command)
            case "history":
                self._handle_history(command)
            case _:
                found_path = self._check_PATH(command[0])
                if found_path:
                    self._run_program(command)
                else:
                    self._handle_unknown_commands(command)

    def _handle_history(self, cmd_name):
        """Display history of commands with proper formatting"""
        memory_len = len(self.prev_cmds)
        if not memory_len:
            return
        if len(cmd_name) > 1:
            try:
                n = int(cmd_name[1])
                if n <= 0:
                    print(f"invalid arg for {command[0]}")
            except ValueError:
                print(f"invalid arg for {command[0]}")
            else:
                start_idx = memory_len-n
        else:
            start_idx = 0
        for i in range(start_idx,memory_len):
            print(f"    {i + 1}  {self.prev_cmds[i]}")


    def _handle_exit(self):
        """Handle exit command"""
        self.running = False

    def _handle_type(self, command):
        """Handle type command"""
        BUILTINS = {"type", "echo", "exit", "pwd", "history"}
        if len(command) < 2:
            print("type: missing argument")
            return

        cmd_name = command[1]
        if cmd_name in BUILTINS:
            print(f'{cmd_name} is a shell builtin')
        else:
            found_path = self._check_PATH(cmd_name)
            if found_path:
                print(f'{cmd_name} is {found_path}')
            else:
                print(f'{cmd_name}: not found')

    def _handle_echo(self, command):
        """Handle echo command"""
        print(" ".join(command[1:]))

    def _handle_unknown_commands(self, command):
        """"Handle unknown commands"""
        print(f'{' '.join(command)}: command not found')

    def _check_PATH(self, cmd_name):
        """Check for executable files in PATH and return the first match"""
        PATH_dirs = os.environ.get("PATH", "").split(":")

        for directory in PATH_dirs:
            if directory:
                full_path = os.path.join(directory, cmd_name)
                if os.path.isfile(full_path):
                    return full_path
        return None

    def _run_program(self, command):
        """Run program"""
        subprocess.run([command[0]] + command[1:])

    def _handle_pwd(self):
        """Print present working directory"""
        print(os.getcwd())

    def _handle_cd(self, command):
        """Changes directory if it exists"""
        if len(command) < 2:
            return

        path = command[1]
        if path == "~":
            home_directory = Path.home()
            os.chdir(home_directory)
            return
        if os.path.isdir(path):
            os.chdir(path)
        else:
            print(f"cd: {path}: No such file or directory")


def main():
    shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
