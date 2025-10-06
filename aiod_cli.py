import argparse
import json
import sys

from auth import get_access_token
from make_req_asset import add_asset, edit_asset

def main():
    parser = argparse.ArgumentParser(description="AIoD metadata catalogue CLI")
    parser.add_argument('--entity', required=True, help="Entity to operate on (e.g. experiment, dataset, etc.)")
    
    #add parse
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add new entity")
    add_parser.add_argument("--data", required=True, type=str, help="Entity metadata in JSON")

    #edit parsers
    edit_parser = subparsers.add_parser("edit", help="Edit existing entity")
    edit_parser.add_argument("--id", required=True, type=str, help="Ientifier of entity to edit")
    edit_parser.add_argument("--data", required=True, type=str, help="Entity metadata in JSON")

    args = parser.parse_args()

    if args.command not in ["add", "edit"]:
        parser.print_help()
        sys.exit(1)

    token_info = get_access_token()
    if token_info is None:
        print("Failed to obtain a valid access token. Exiting.")
        sys.exit(1)

    access_token = token_info["access_token"]

    try: 
        entity_type = args.entity
        entity_data = json.loads(args.data)
        edit_id = args.id if args.command == 'edit' else None
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        exit(1)
    if args.command == "add":
        add_asset(entity_type, entity_data, access_token)
    elif args.command == "edit":
        edit_asset(entity_type, entity_data, access_token, edit_id)

if __name__ == "__main__":
    main()