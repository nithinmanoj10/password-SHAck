import os

from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    os.system("clear")

    console.print("Welcome to password-SHAck\n", style="bold yellow")

    console.print("[black][1][/black] Sign up and create new vault")
    console.print("[black][2][/black] Login and view vault")

    menu_option = int(Prompt.ask("\nEnter your option", choices=["1", "2"]))
    print(menu_option)

if __name__ == "__main__":
    main()