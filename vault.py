import sys
import random
import hashlib
import string

import mysql.connector

from rich import print as printc
from rich.console import Console

from getpass import getpass

console = Console()

def connect_to_vault():
    try:
        db = mysql.connector.connect(
        host ="localhost",
        user ="password-shack",
        passwd ="gna"
        )
    except Exception as e:
        console.log("[red]An error occurred while trying to connect to the vault[/red]")
        quit()

    return db

def does_vault_exists():
    db = connect_to_vault()
    cursor = db.cursor()
    
    query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'password_shack'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    db.close()
    
    if len(results)!=0:
        return True
    
    return False

# TODO: Make a better device secret generator
def generateDeviceSecret(length=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def create():
    print("\n")
    if does_vault_exists():
        console.log("Vault [yellow]password_shack[/yellow] already exists")
        return
    
    console.log("Creating new vault: [yellow]password_shack[/yellow]")
    
    # Creating the vault
    db = connect_to_vault()
    cursor = db.cursor()
    
    try:
        cursor.execute("CREATE DATABASE password_shack")
    except Exception as e:
        console.log("[red]You have already created a vault named [yellow]password_shack[/yellow]")
        quit()
    
    console.log("Vault [yellow]password_shack[/yellow] successfully created")
    
    # Create vault master key table
    query = "CREATE TABLE password_shack.master_key (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)

    query = "CREATE TABLE password_shack.website_passwords (website_name TEXT NOT NULL, website_url TEXT, username TEXT NOT NULL, password TEXT NOT NULL)"
    res = cursor.execute(query)
    
    query = "CREATE TABLE password_shack.email_passwords (email_id TEXT NOT NULL, password TEXT NOT NULL)"
    res = cursor.execute(query)
    
    console.log("Vault shelves for [yellow]password_shack[/yellow] successfully created")
    
    console.log("User needs to enter a master password for vault [yellow]password_shack[/yellow]")
    
    # TODO:
    # 1. Make getting the master password a different function
    # 2. Check if the master password the user entered is strong or not
    
    master_password = None
    is_valid_password = False
    while not is_valid_password:
        console.log("Enter Master Password: ")
        master_password = getpass()
        console.log("Re-enter Master Password: ")
        re_master_password = getpass()
        
        if master_password == re_master_password and master_password != "":
            is_valid_password = True
        else:
            console.log("Master Password doesn't match. Re-enter")
    
    # hashing the master password
    # TODO: Use Argon2 instead
    hashed_mp = hashlib.sha256(master_password.encode()).hexdigest()
    
    device_secret = generateDeviceSecret()
    
    query = "INSERT INTO password_shack.master_key (masterkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, device_secret)
    cursor.execute(query, val)
    db.commit()

    console.log("[yellow]password_shack[/yellow] vault creation completed")

    db.close()

    
if __name__ == '__main__':
    globals()[sys.argv[1]]()