''' Determine terminal foreground and background colors

    Source: https://jwodder.github.io/kbits/posts/term-fgbg/
    John T. Wodder II, CC-BY-4.0
'''
from __future__ import annotations
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
import re
import sys
import termios


def parse_color(color):
    if color.startswith('rgb:'):
        rgb = f'#{color[4:6]}{color[9:11]}{color[14:16]}'
    else:
        rgb = None
    return rgb


def get_default_fg() -> str:
    """
    Query the attached terminal for the default foreground color and return the
    color string from the response

    :raises IOError: if stdin or stdout is not a terminal
    :raises ValueError: if the reply from the terminal is malformed
    """
    try:
        color = osc_query(10)
    except (ValueError, IOError):
        return None
    else:
        return parse_color(color)


def get_default_bg() -> str:
    """
    Query the attached terminal for the default background color and return the
    color string from the response

    :raises IOError: if stdin or stdout is not a terminal
    :raises ValueError: if the reply from the terminal is malformed
    """
    try:
        color = osc_query(11)
    except (ValueError, IOError):
        return None
    else:
        return parse_color(color)


def osc_query(ps: int) -> str:
    if sys.stdin.isatty() and sys.stdout.isatty():
        with cbreak_noecho():
            print(f"\x1b]{ps};?\x1b\\", end="", flush=True)
            resp = b""
            while not resp.endswith((b"\x1b\\", b"\x07")):
                resp += sys.stdin.buffer.read(1)
        s = resp.decode("utf-8", "surrogateescape")
        if m := re.fullmatch(rf"\x1B\]{ps};(.+)(?:\x1B\\|\x07)", s):
            return m[1]
        else:
            raise ValueError(s)
    else:
        raise IOError("not connected to a terminal")


# File descriptor for standard input:
STDIN = 0

# Indices into the tuple returned by `tcgetattr()`:
LFLAG = 3
CC = 6


@contextmanager
def cbreak_noecho() -> Iterator[None]:
    """
    A context manager that configures the terminal on standard input to use
    cbreak mode and to disable input echoing.  The original terminal
    configuration is restored on exit.
    """
    orig = termios.tcgetattr(STDIN)
    term = deepcopy(orig)
    term[LFLAG] &= ~(termios.ICANON | termios.ECHO)
    term[CC][termios.VMIN] = 1
    term[CC][termios.VTIME] = 0
    termios.tcsetattr(STDIN, termios.TCSANOW, term)
    try:
        yield
    finally:
        termios.tcsetattr(STDIN, termios.TCSANOW, orig)


if __name__ == "__main__":
    print("Foreground color:", get_default_fg())
    print("Background color:", get_default_bg())
