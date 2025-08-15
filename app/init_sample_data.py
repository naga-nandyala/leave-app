#!/usr/bin/env python3
"""
Sample data initialization script for Team Availability App
Run this script to populate the app with sample data for testing
"""

import json
import os
from datetime import datetime, timedelta


def create_sample_data():
    """Create sample data for the team availability app"""

    # Create data directory
    os.makedirs("data", exist_ok=True)

    # Sample team members
    members_data = {
        "1": {"name": "Naga", "country": "Australia", "region": "NSW"},
        "2": {"name": "Anuj", "country": "Australia", "region": "VIC"},
        "3": {"name": "Teresa", "country": "Australia", "region": "WA"},
        "4": {"name": "Xing", "country": "China", "region": "Shanghai"},
        "5": {"name": "Hang", "country": "China", "region": "Shanghai"},
        "6": {"name": "Jeffery", "country": "USA", "region": "California"},
    }

    # Sample holidays
    holidays_data = {
        "national": {
            "Australia": {
                "2025-01-01": "New Year's Day",
                "2025-01-26": "Australia Day",
                "2025-04-25": "ANZAC Day",
                "2025-12-25": "Christmas Day",
                "2025-12-26": "Boxing Day",
            },
            "China": {
                "2025-01-01": "New Year's Day",
                "2025-02-10": "Chinese New Year",
                "2025-02-11": "Chinese New Year",
                "2025-02-12": "Chinese New Year",
                "2025-05-01": "Labour Day",
                "2025-10-01": "National Day",
            },
            "USA": {
                "2025-01-01": "New Year's Day",
                "2025-01-20": "Martin Luther King Jr. Day",
                "2025-02-17": "Presidents Day",
                "2025-05-26": "Memorial Day",
                "2025-07-04": "Independence Day",
                "2025-09-01": "Labor Day",
                "2025-11-27": "Thanksgiving Day",
                "2025-12-25": "Christmas Day",
            },
        },
        "regional": {
            "Australia": {
                "NSW": {"2025-06-09": "Queen's Birthday (NSW)", "2025-10-06": "Labour Day (NSW)"},
                "VIC": {
                    "2025-03-10": "Labour Day (VIC)",
                    "2025-06-09": "Queen's Birthday (VIC)",
                    "2025-11-04": "Melbourne Cup Day",
                },
                "WA": {
                    "2025-03-03": "Labour Day (WA)",
                    "2025-06-02": "Western Australia Day",
                    "2025-09-29": "Queen's Birthday (WA)",
                },
            },
            "China": {
                "Shanghai": {
                    "2025-04-05": "Qingming Festival",
                    "2025-06-12": "Dragon Boat Festival",
                    "2025-09-17": "Mid-Autumn Festival",
                },
            },
            "USA": {
                "California": {"2025-03-31": "Cesar Chavez Day", "2025-11-28": "Day after Thanksgiving"},
            },
        },
    }

    # Sample out of office entries
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    next_month = today + timedelta(days=30)

    ooo_data = {
        "1": [{"start_date": str(next_week), "end_date": str(next_week + timedelta(days=4)), "reason": "Vacation"}],
        "3": [{"start_date": str(next_month), "end_date": str(next_month + timedelta(days=2)), "reason": "Conference"}],
        "6": [
            {
                "start_date": str(today + timedelta(days=14)),
                "end_date": str(today + timedelta(days=16)),
                "reason": "Personal",
            }
        ],
    }

    # Save data to files
    with open("data/members.json", "w") as f:
        json.dump(members_data, f, indent=2)

    with open("data/holidays.json", "w") as f:
        json.dump(holidays_data, f, indent=2)

    with open("data/ooo.json", "w") as f:
        json.dump(ooo_data, f, indent=2, default=str)

    print("Sample data created successfully!")
    print("\nSample team members added:")
    for member_id, member in members_data.items():
        print(f"- {member['name']} ({member['country']}, {member['region']})")

    print("\nSample holidays added for Australia, China, and USA")
    print("Sample out of office entries added for some team members")
    print("\nYou can now run the app with: python app.py")


if __name__ == "__main__":
    create_sample_data()
