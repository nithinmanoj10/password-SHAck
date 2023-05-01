import os
import sys
import subprocess

from rich.console import Console 
from rich.prompt import Prompt

console = Console()

def file_is_setup() -> bool:
    '''
        Checks if the file system is already setup
        or not. Does this by checking if the master_info.txt
        exists or not.
    '''

    master_path = "./master_info.txt"
    check_file = os.path.isfile(master_path)
    return check_file

def is_pre_req_installed(pre_req_name) -> bool:
    pip_result = subprocess.run(["which", pre_req_name], stdout=subprocess.PIPE).stdout.decode("utf-8")

    if pip_result != '':
        return True
    
    return False

def is_venv_installed() -> bool:
    try:
        import virutalenv
    except:
        return False
    
    return True

def print_pre_requisite_exists(does_exists, pre_req_name):
    if does_exists:
        console.print("[[✓][/green] " + pre_req_name)
    else:
        console.print("[red][X][/red] " + pre_req_name)

def setup():
    os.system("clear")

    console.print("🗃️ Setting up password-SHAck\n", style="bold yellow")

    # console.print("[bold yellow]password-SHAck[/bold yellow] requires [bold cyan]python3[/bold cyan] and [bold cyan]pip3[/bold cyan] to be installed as pre-requisites")
    # console.print("As of now the following are already installed on your machine\n")

    # python3_exists = is_pre_req_installed("python3")
    # pip_exists = is_pre_req_installed("pip3")

    # console.print_pre_requisite_exists(python3_exists, "python3.8")
    # console.print_pre_requisite_exists(pip_exists, "pip3")

    # if not python3_exists or not pip_exists:
    #     console.print("\n[red]Error[/red] Please install the necessary pre-requisites and try running the setup again\n")

    #     console.print("[bold black][·][/bold black] For installing [bold cyan]python3.8[/bold cyan] visit: [bold black][link=https://phoenixnap.com/kb/how-to-install-python-3-ubuntu]Install python3 on Ubuntu[/link][/bold black]")
    #     console.print("[bold black][·][/bold black] For installing [bold cyan]pip3[/bold cyan] visit: [bold black][link=https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/]Install pip on Ubuntu[/link][/bold black]")

    #     Prompt.ask("\nHit enter to exit setup")
    #     console.print("\n[black]Exiting setup.py[/black]", style="bold")
    #     sys.exit()
    # else:
    #     console.print("\n[bold yellow]password-SHAck[/bold yellow] will be running in a virtual environment named [bold green](password-shack)[/bold green]")
    #     console.print("For this, we shall be installing the [bold cyan]virtualenv[/bold cyan] library using [bold cyan]pip3[/bold cyan]\n")

    #     Prompt.ask("Hit enter to install [bold cyan]virtualenv[/bold cyan]")
    #     console.print("")

    #     os.system("pip3 install virtualenv")

    #     console.print("\nYou are also needed to install [bold cyan]python3.8-venv[/bold cyan]. The following command will be executed and")
    #     console.print("you will be prompted to enter your root password to install it\n")

    #     console.print("$ sudo apt install python3.8-venv\n", style="bold black")
    #     Prompt.ask("Hit enter to install [bold cyan]python3.8-venv[/bold cyan]")
    #     console.print("")

    #     os.system("sudo apt install python3.8-venv")

    #     console.print("\nNow we will create the python virtual environment [bold green](password-shack)[/bold green] and activate it")

    #     Prompt.ask("Hit enter to create and activate [bold green](password-shack)[/bold green]")
    #     console.print("")

    #     os.system("python3.8 -m venv password-shack")
    #     os.system(". password-shack/bin/activate")

    #     console.print("[bold yellow]password-SHAck[/bold yellow] will be running inside [bold green](password-shack)[/bold green] virtual environment.")
    #     console.print("The following packages will be installed using [bold cyan]pip3[/bold cyan] so that [bold yellow]password-SHAck[/bold yellow] can be used without any errors\n")

    #     console.print("[bold black][·][/bold black] rich")


    if not file_is_setup():
        console.print("The following file and directory will be created \n")
        console.print("[green][+][/green] master_info.txt")
        console.print("[green][+][/green] vaults")

        continue_with_setup = Prompt.ask("\nWould you like to continue with the setup process?", choices=["y", "n"], default="y")
        
        if continue_with_setup == "y":
            # creating the master_info.txt file
            with open('master_info.txt', "w") as f:
                pass

            # creating the vaults directory
            os.system("mkdir vaults")

            console.print("\n[green][✓][/green] Setup process completed")
    else:
        console.print("Looks like you have setup the necessary files for [bold yellow]password-SHAck[/bold yellow].")
        Prompt.ask("Hit enter to exit the setup process")

    console.print("\n[black]Exiting setup.py[/black]", style="bold")

if __name__ == "__main__":
    setup()