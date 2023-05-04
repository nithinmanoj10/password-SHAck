import sys
import random
import hashlib
import string

import mysql.connector

from rich import print as printc
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table
from rich import inspect

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

from getpass import getpass
from utils import otp_generator
from input_check import check_entry
from encrypt_utils import encrypt, decrypt

console = Console()


def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="localhost", user="password-shack", passwd="gna"
        )
    except Exception as e:
        console.log("[red]An error occurred while trying to connect to the vault[/red]")
        quit()

    return db


def does_vault_exists(vault_name):
    db = connect_to_db()
    cursor = db.cursor()

    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = '{vault_name}'"
    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    if len(results) != 0:
        return True

    return False


def get_all_vaults_name():
    db = connect_to_db()
    cursor = db.cursor()

    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    return results


# TODO: Make a better device secret generator
def generateDeviceSecret(length=10):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_vault(vault_name):
    print("\n")
    if does_vault_exists(vault_name):
        console.log(f"Vault [yellow]{vault_name}[/yellow] already exists")
        return

    console.log(f"Creating new vault: [yellow]{vault_name}[/yellow]")

    # Creating the vault
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {vault_name}")
    except Exception as e:
        console.log(
            f"[red]You have already created a vault named [yellow]{vault_name}[/yellow]"
        )
        quit()

    console.log(f"Vault [yellow]{vault_name}[/yellow] successfully created")

    # Create vault master key table
    query = f"CREATE TABLE {vault_name}.master_key (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)

    query = f"CREATE TABLE {vault_name}.website_passwords (website_name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)"
    res = cursor.execute(query)

    console.log(f"Vault shelves for [yellow]{vault_name}[/yellow] successfully created")

    console.log(
        f"User needs to enter a master password for vault [yellow]{vault_name}[/yellow]"
    )

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

    query = f"INSERT INTO {vault_name}.master_key (masterkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, device_secret)
    cursor.execute(query, val)
    db.commit()

    console.log(f"[yellow]{vault_name}[/yellow] vault creation completed")

    db.close()


def verify_master_password(vault_name):
    
    console.log(f"Enter your master password for [yellow]{vault_name}[/yellow]")
    master_password = getpass("Master password: ")

    hashed_mp = hashlib.sha256(master_password.encode()).hexdigest()

    db = connect_to_db()
    cursor = db.cursor()
    query = f"SELECT * FROM {vault_name}.master_key"
    cursor.execute(query)
    result = cursor.fetchall()[0]

    if hashed_mp != result[0]:
        console.log("[red]You have entered the wrong master password[/red]")
        return None

    return [master_password, result[1]]

def delete_vault(vault_name):
    if not does_vault_exists(vault_name):
        console.log(
            f"[red]Error[/red]: Vault [yellow]{vault_name}[/yellow] does not exists"
        )
        return

    console.log(
        "[red]Deleting a vault can have serious consequences. You will lose all of your stored passwords.[/red]"
    )

    verify_master_password(vault_name)

    otp_attempts = 0
    is_correct = False

    while otp_attempts < 3:
        otp = otp_generator()
        first_half, sec_half = str(otp)[:3], str(otp)[3:]
        console.log(f"Attempts remaining: [red]{3-otp_attempts}[/red]")
        console.log(
            f"Enter the following 6-digit pin: [yellow bold]{first_half} {sec_half}[/yellow bold]"
        )

        console.print("[cyan bold]OTP: [/cyan bold]", end="")
        input_otp = int(input())

        if input_otp == otp:
            is_correct = True
            break
        else:
            otp_attempts += 1

    if not is_correct:
        console.log("User did not enter the right OTP")
        console.log("Exiting the program")
        return

    db = connect_to_db()
    cursor = db.cursor()

    query = f"DROP DATABASE {vault_name}"
    cursor.execute(query)
    db.commit()
    db.close()

    console.log(f"Vault [yellow]{vault_name}[/yellow] deleted")


def list_vaults():
    results = get_all_vaults_name()
    non_vaults = ["information_schema", "performance_schema", "mysql"]

    table = Table()
    table.add_column("Vault Name", justify="left", style="cyan", no_wrap=True)

    for vault in results:
        vault_name = vault[0]
        if vault_name not in non_vaults:
            table.add_row(vault_name)

    console.print(table)


def add_to_vault(master_password, device_salt, args):
    username, sitename = args.username, args.site_name
    
    # check if entry already exists
    if check_entry(args.vault_name, sitename, username):
        console.log(f'Vault {args.vault_name} already has entry for {sitename}:{username}')
        return
    
    password = getpass("Enter password: ")
    
    master_key = compute_master_key(master_password, device_salt)
    
    encrypted = encrypt(master_key, password, True, "bytes")
    
    # Add to db
    db = connect_to_db()
    cursor = db.cursor()
    query = f'INSERT INTO {args.vault_name}.website_passwords (website_name, username, password) values (%s, %s, %s)'
    val = (sitename,username,encrypted)
    cursor.execute(query, val)
    db.commit()
    
    console.log(f"Password added to {args.vault_name}")

# TODO: Add for Argon2
def compute_master_key(master_password, device_salt):
    password = master_password.encode()
    salt = device_salt.encode()
    
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def view_vault(master_password, device_salt, args):
    db = connect_to_db()
    cursor = db.cursor()

    query = f'SELECT * FROM {args.vault_name}.website_passwords WHERE website_name = \'{args.site_name}\' AND username = \'{args.username}\''

    cursor.execute(query)
    results = cursor.fetchall()
    
    if len(results) == 0:
        console.log("The record you were searching for doesn't exists")
        return
    
    master_key = compute_master_key(master_password, device_salt)
    decrypted_password = decrypt(master_key, results[0][2], True, "bytes")
    
    console.log(f'Your password: {decrypted_password.decode()}')