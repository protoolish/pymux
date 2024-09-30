#!/usr/bin/env python3

from os import system, environ
from typing import Dict

class Tmux:
    def __init__(self, name: str, dir: str, venv: str = None):
        self._name = name
        self._dir = dir
        self._venv = venv

    @staticmethod
    def tmux(command: str): system(f"tmux {command}")

class Window(Tmux):
    def send(self, command: str, enter = True):
        self.tmux(f"send -t {self._name} \"{command}\" {'C-m' if enter else ''}")

class Session(Tmux):
    def __init__(self, name: str, dir = environ.get("HOME"), venv: str = None):
        super().__init__(name, dir, venv)
        self._windows: Dict[str, Window] = {}

        self.new_window("term")

    def send(self, window: str, command: str, enter = True):
        return self._windows[window].send(command, enter)

    def new_window(self, name: str) -> Window:

        if not self._windows:
            self.tmux(f"new -d -c \"{self._dir}\" -s \"{self._name}\" -n \"{name}\"")
        else:
            self.tmux(f"new-window -a -c \"{self._dir}\" -t \"{self._name}\" -n {name}")

        res = Window(f"{self._name}:{len(self._windows)}.0", self._dir, self._venv)
        if self._venv: res.send(f"workon {self._venv}")

        self._windows[name] = res
        return res