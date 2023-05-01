from argparse import ArgumentParser

from vault import create_vault

parser = ArgumentParser(
    description="Welcome to password-SHAck command line interface.\nYou can create your own secure vault to store and retrieve your passwords."
)
parser.add_argument(
    'vault_action',
    help="(c)reate | (a)dd | (v)iew | (d)elete",
)

parser.add_argument(
    'vault_name',
    help="Name of the vault",
)

args = parser.parse_args()

def main():
    
    # creating a new vault
    if args.vault_action in ["create", "c"]:
        create_vault(args.vault_name)
        
main()