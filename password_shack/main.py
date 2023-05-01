import os

from rich.console import Console
from rich.prompt import Prompt

console = Console()

from menu import login_user


def main():
    login_user()


if __name__ == "__main__":
    main()
