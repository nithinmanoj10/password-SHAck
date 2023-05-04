import hashlib

from rich import inspect
from rich.console import Console
import mysql.connector

console = Console()

from getpass import getpass

def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="localhost", user="password-shack", passwd="gna"
        )
    except Exception as e:
        console.log("[red]An error occurred while trying to connect to the vault[/red]")
        quit()

    return db


def is_valid_add_query(args):
    is_valid = True
    if args.site_name == None:
        console.log("Please provide a site name (-S site_name)")
        is_valid = False
    if args.username == None:
        console.log("Please provide a username (-U username)")
        is_valid = False

    return is_valid


def validate_master_password(args):
    vault_name = args.vault_name
    console.log(f"Enter your master password for [yellow]{vault_name}[/yellow]")
    master_password = getpass("Master password: ")

    hashed_mp = hashlib.sha256(master_password.encode()).hexdigest()

    db = connect_to_db()
    cursor = db.cursor()
    query = f"SELECT * FROM {args.vault_name}.master_key"
    cursor.execute(query)
    result = cursor.fetchall()[0]

    if hashed_mp != result[0]:
        console.log("[red]You have entered the wrong master password[/red]")
        return None

    return [master_password, result[1]]


def check_entry(vault_name, sitename, username):
    db = connect_to_db()

    cursor = db.cursor()
    query = f"SELECT * FROM {vault_name}.website_passwords WHERE website_name = '{sitename}' AND username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) != 0:
        return True

    return False
