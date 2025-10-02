import argparse
import json
import sys

from auth import get_access_token, refresh_token
from make_req_asset import add_asset, edit_asset
# from make_req_edit_asset import edit_asset

def main():
    parser = argparse.ArgumentParser(description="AIoD metadata catalogue CLI")
    parser.add_argument('--entity', required=True, help="Entity to work on (ej: experiment, dataset, etc.)")
    
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser('add', help='Add new asset')
    add_parser.add_argument('--data', required=True, type=str, help='Asset`s metadata in JSON format')

    edit_parser = subparsers.add_parser('edit', help='Edit existing asset')
    edit_parser.add_argument('--data', required=True, type=str, help='Asset`s metadata in JSON format')

    args = parser.parse_args()

    if args.command not in ['add', 'edit']:
        parser.print_help()
        sys.exit(1)

    token_info = get_access_token()
    if token_info is None:
        print("Can not get a valid token. Exiting.")
        sys.exit(1)

    access_token = token_info["access_token"]

    try: 
        entity_type = args.entity
        entity_data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        exit(1)
    if args.command == 'add':
        add_asset(entity_type, entity_data, access_token)
    elif args.command == 'edit':
        edit_asset(entity_type, entity_data, access_token)

if __name__ == "__main__":
    main()