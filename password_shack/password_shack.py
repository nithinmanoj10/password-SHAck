from argparse import ArgumentParser

from vault import create_vault, delete_vault, list_vaults

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
        
        
main()