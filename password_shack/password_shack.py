from argparse import ArgumentParser

from vault import create_vault, delete_vault, list_vaults, add_to_vault, view_vault
from input_check import is_valid_add_query, validate_master_password

from rich.pretty import pprint

parser = ArgumentParser(
    description="Welcome to password-SHAck command line interface.\nYou can create your own secure vault to store and retrieve your passwords."
)
parser.add_argument(
    '-L',
    '--list',
    help="List all of the vaults",
    action="store_true"
)
parser.add_argument(
    'vault_action',
    help="(c)reate | (a)dd | (v)iew | (d)elete",
    nargs='?',
    default="c",
)

parser.add_argument(
    'vault_name',
    help="Name of the vault",
    nargs='?',
    default="shack",
)

parser.add_argument(
    '-S',
    '--site_name',
    help="Name of the site",
    metavar="site_name"
)

parser.add_argument(
    '-U',
    '--username',
    help="Username used in the site login",
    metavar="user_name"
)

args = parser.parse_args()

def main():
        
    if args.list:
        list_vaults()
        return
        
    # creating a new vault
    if args.vault_action in ["create", "c"]:
        create_vault(args.vault_name)
        return
        
    if args.vault_action in ["delete", "d"]:
        
        delete_vault(args.vault_name)
        return
    
    # adding a password
    if args.vault_action in ["add", "a"]:
        if not is_valid_add_query(args):
            return
        
        result = validate_master_password(args)
        
        if result is not None:
            add_to_vault(result[0], result[1], args)
            
        return
    
    # viewing a password
    if args.vault_action in ["view", "v"]:
        if not is_valid_add_query(args):
            return
        
        result = validate_master_password(args)
        
        if result is not None:
            view_vault(result[0], result[1], args)
        
        
main()