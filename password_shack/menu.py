"""
Module that deals with logging in or creating a new account
for a user that uses the password manager
"""

import os

from rich.console import Console
from rich.prompt import Prompt

console = Console()

login_options = ["Sign up and create new vault", "Login and view vault", "Quit"]


def login_user():
    """
        Displays the login menu and does what the user chooses to do.
        User could login and view their passwords, sign up to create
        a new vault or quit the application
    """
    
    option = login_menu()
    login_action(option)
    

def login_menu() -> int:
    """
        Displays the login menu screen and prompts the user to
        choose their option
        
        returns:
            option: int     The option choosen by the user 
    """
    os.system("clear")

    console.print("Welcome to password-SHAck\n", style="bold yellow")

    for opt_num, option in enumerate(login_options):
        console.print(f"[black][{opt_num+1}][/black] {option}")

    menu_option = int(Prompt.ask("\nEnter your option", choices=["1", "2", "3"]))

    return menu_option

def login_action(option: int):
    """
        Does the action based on the option choosen by the user
    """
    
    # sign up user
    if option == 1:
        pass
    
    # login user
    if option == 2:
        pass
    
    # quit
    if option == 3:
        quit_program() 
        
def quit_program():
    console.print("\nClosing [bold yellow]password-SHAck[/bold yellow]\n")
    quit()