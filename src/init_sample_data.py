#!/usr/bin/env python3
"""
Sample data initialization script for Team Availability App
Run this script to populate the app with sample data for testing
"""

import json
import os


def create_data_files():
    """Create data files with proper structure"""

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create directories relative to script location
    data_dir = os.path.join(script_dir, "data")
    config_dir = os.path.join(script_dir, "config")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

    # Members data (empty by default)
    members = {}

    # Holidays data (empty structure)
    holidays = {"national": {}, "regional": {}}

    # Out of office data (empty by default)
    ooo = {}

    # History data (empty list)
    history = []

    # Countries configuration
    countries = {
        "countries": {
            "AU": {"name": "Australia", "code": "AU"},
            "CN": {"name": "China", "code": "CN"},
            "US": {"name": "United States", "code": "US"},
        }
    }

    # Save files using absolute paths
    with open(os.path.join(data_dir, "members.json"), "w") as f:
        json.dump(members, f, indent=2)

    with open(os.path.join(data_dir, "holidays.json"), "w") as f:
        json.dump(holidays, f, indent=2)

    with open(os.path.join(data_dir, "ooo.json"), "w") as f:
        json.dump(ooo, f, indent=2)

    with open(os.path.join(data_dir, "history.json"), "w") as f:
        json.dump(history, f, indent=2)

    with open(os.path.join(config_dir, "countries.json"), "w") as f:
        json.dump(countries, f, indent=2)

    print("Data files created successfully!")


if __name__ == "__main__":
    create_data_files()
