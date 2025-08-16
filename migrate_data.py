#!/usr/bin/env python3
"""
Data Migration Utility for Leave App
Helps migrate data between local storage and Azure Blob Storage
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

# Add src directory to path to import storage_manager
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from storage_manager import LocalFileStorage, AzureBlobStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_FILES = ["holidays.json", "members.json", "ooo.json", "history.json"]


def migrate_local_to_azure(local_data_dir: str, azure_account: str, azure_container: str = "leaveapp-data"):
    """Migrate data from local storage to Azure Blob Storage"""
    logger.info(f"Starting migration from local storage to Azure...")

    # Initialize storage managers
    local_storage = LocalFileStorage(local_data_dir)
    azure_storage = AzureBlobStorage(azure_account, azure_container)

    migration_summary = {"success": [], "failed": [], "skipped": []}

    for filename in DATA_FILES:
        try:
            if local_storage.file_exists(filename):
                # Load data from local storage
                data = local_storage.load_data(filename)

                # Save to Azure storage
                success = azure_storage.save_data(filename, data)

                if success:
                    migration_summary["success"].append(filename)
                    logger.info(f"✓ Migrated {filename}")
                else:
                    migration_summary["failed"].append(filename)
                    logger.error(f"✗ Failed to migrate {filename}")
            else:
                migration_summary["skipped"].append(filename)
                logger.info(f"- Skipped {filename} (not found)")

        except Exception as e:
            migration_summary["failed"].append(f"{filename} ({str(e)})")
            logger.error(f"✗ Error migrating {filename}: {e}")

    print("\n" + "=" * 50)
    print("MIGRATION SUMMARY")
    print("=" * 50)
    print(f"Successfully migrated: {len(migration_summary['success'])} files")
    for file in migration_summary["success"]:
        print(f"  ✓ {file}")

    if migration_summary["failed"]:
        print(f"\nFailed to migrate: {len(migration_summary['failed'])} files")
        for file in migration_summary["failed"]:
            print(f"  ✗ {file}")

    if migration_summary["skipped"]:
        print(f"\nSkipped: {len(migration_summary['skipped'])} files")
        for file in migration_summary["skipped"]:
            print(f"  - {file}")

    return len(migration_summary["failed"]) == 0


def migrate_azure_to_local(azure_account: str, local_data_dir: str, azure_container: str = "leaveapp-data"):
    """Migrate data from Azure Blob Storage to local storage"""
    logger.info(f"Starting migration from Azure to local storage...")

    # Initialize storage managers
    azure_storage = AzureBlobStorage(azure_account, azure_container)
    local_storage = LocalFileStorage(local_data_dir)

    migration_summary = {"success": [], "failed": [], "skipped": []}

    # Get list of files from Azure
    azure_files = azure_storage.list_files()

    for filename in DATA_FILES:
        try:
            if filename in azure_files:
                # Load data from Azure storage
                data = azure_storage.load_data(filename)

                # Save to local storage
                success = local_storage.save_data(filename, data)

                if success:
                    migration_summary["success"].append(filename)
                    logger.info(f"✓ Migrated {filename}")
                else:
                    migration_summary["failed"].append(filename)
                    logger.error(f"✗ Failed to migrate {filename}")
            else:
                migration_summary["skipped"].append(filename)
                logger.info(f"- Skipped {filename} (not found in Azure)")

        except Exception as e:
            migration_summary["failed"].append(f"{filename} ({str(e)})")
            logger.error(f"✗ Error migrating {filename}: {e}")

    print("\n" + "=" * 50)
    print("MIGRATION SUMMARY")
    print("=" * 50)
    print(f"Successfully migrated: {len(migration_summary['success'])} files")
    for file in migration_summary["success"]:
        print(f"  ✓ {file}")

    if migration_summary["failed"]:
        print(f"\nFailed to migrate: {len(migration_summary['failed'])} files")
        for file in migration_summary["failed"]:
            print(f"  ✗ {file}")

    if migration_summary["skipped"]:
        print(f"\nSkipped: {len(migration_summary['skipped'])} files")
        for file in migration_summary["skipped"]:
            print(f"  - {file}")

    return len(migration_summary["failed"]) == 0


def list_files(storage_type: str, **kwargs):
    """List files in storage"""
    if storage_type == "local":
        local_dir = kwargs.get("local_dir", "./src/data")
        storage = LocalFileStorage(local_dir)
        files = storage.list_files()
        print(f"\nFiles in local storage ({local_dir}):")
    elif storage_type == "azure":
        azure_account = kwargs.get("azure_account")
        azure_container = kwargs.get("azure_container", "leaveapp-data")
        storage = AzureBlobStorage(azure_account, azure_container)
        files = storage.list_files()
        print(f"\nFiles in Azure storage ({azure_account}/{azure_container}):")

    if files:
        for file in files:
            print(f"  • {file}")
    else:
        print("  No files found")


def main():
    parser = argparse.ArgumentParser(description="Migrate data between local and Azure storage")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Local to Azure migration
    local_to_azure = subparsers.add_parser("local-to-azure", help="Migrate from local to Azure")
    local_to_azure.add_argument("--local-dir", default="./src/data", help="Local data directory")
    local_to_azure.add_argument("--azure-account", required=True, help="Azure storage account name")
    local_to_azure.add_argument("--azure-container", default="leaveapp-data", help="Azure container name")

    # Azure to local migration
    azure_to_local = subparsers.add_parser("azure-to-local", help="Migrate from Azure to local")
    azure_to_local.add_argument("--azure-account", required=True, help="Azure storage account name")
    azure_to_local.add_argument("--azure-container", default="leaveapp-data", help="Azure container name")
    azure_to_local.add_argument("--local-dir", default="./src/data", help="Local data directory")

    # List files
    list_cmd = subparsers.add_parser("list", help="List files in storage")
    list_cmd.add_argument("storage_type", choices=["local", "azure"], help="Storage type")
    list_cmd.add_argument("--local-dir", default="./src/data", help="Local data directory (for local storage)")
    list_cmd.add_argument("--azure-account", help="Azure storage account name (for Azure storage)")
    list_cmd.add_argument("--azure-container", default="leaveapp-data", help="Azure container name (for Azure storage)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "local-to-azure":
            success = migrate_local_to_azure(args.local_dir, args.azure_account, args.azure_container)
            sys.exit(0 if success else 1)

        elif args.command == "azure-to-local":
            success = migrate_azure_to_local(args.azure_account, args.local_dir, args.azure_container)
            sys.exit(0 if success else 1)

        elif args.command == "list":
            if args.storage_type == "azure" and not args.azure_account:
                print("Error: --azure-account is required for Azure storage")
                sys.exit(1)

            list_files(
                args.storage_type,
                local_dir=args.local_dir,
                azure_account=args.azure_account,
                azure_container=args.azure_container,
            )

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
