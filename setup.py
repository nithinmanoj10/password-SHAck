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

def is_conda_installed() -> bool:
    '''
        Checks whether conda is installed in the Linux
        machine of the user. Conda is used to create
        a virtual environment for password-SHAck.

        This is achieved by running the following command:
        $ which conda

        The above command returns the path of installed conda 
        if it exists, else it returns an empty string

        Returns:

            True:   if conda is installed
            False:  if conda is not installed
    '''
    conda_result = subprocess.run(["which", "conda"], stdout=subprocess.PIPE).stdout.decode("utf-8")

    if conda_result != '':
        return True
    
    return False

def is_pip_installed() -> bool:
    '''
        Checks whether pip is installed in the Linux
        machine of the user. pip is used for installing
        python packages used by password-SHAck.

        This is achieved by running the following command:
        $ which pip

        The above command returns the path of installed conda 
        if it exists, else it returns an empty string

        Returns:

            True:   if pip is installed
            False:  if pip is not installed
    '''
    pip_result = subprocess.run(["which", "pip3"], stdout=subprocess.PIPE).stdout.decode("utf-8")

    if pip_result != '':
        return True
    
    return False

def print_pre_requisite_exists(does_exists, pre_req_name):
    if does_exists:
        console.print("[green][✓][/green] " + pre_req_name)
    else:
        console.print("[red][X][/red] " + pre_req_name)

def setup():
    os.system("clear")

    console.print("🗃️ Setting up password-SHAck\n", style="bold yellow")

    console.print("[bold yellow]password-SHAck[/bold yellow] requires [bold cyan]conda[/bold cyan] and [bold cyan]pip3[/bold cyan] to be installed as pre-requisites")
    console.print("As of now the following are already installed on your machine\n")

    conda_exists = is_conda_installed()
    pip_exists = is_pip_installed()

    print_pre_requisite_exists(conda_exists, "conda")
    print_pre_requisite_exists(pip_exists, "pip3")

    if not conda_exists or not pip_exists:
        console.print("\n[red]Error[/red] Please install the necessary pre-requisites and try running the setup again\n")

        console.print("[bold black][·][/bold black] For installing [bold cyan]conda[/bold cyan] visit: [bold black][link=https://docs.anaconda.com/anaconda/install/linux/]conda installer for Linux[/link][/bold black]")
        console.print("[bold black][·][/bold black] For installing [bold cyan]pip3[/bold cyan] visit: [bold black][link=https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/]Install pip on Ubuntu[/link][/bold black]")

        Prompt.ask("\nHit enter to exit setup")
        console.print("\n[black]Exiting setup.py[/black]", style="bold")
        sys.exit()

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

            console.print("[green][✓][/green] Setup process completed")

    console.print("\n[black]Exiting setup.py[/black]", style="bold")

if __name__ == "__main__":
    setup()