#!/usr/bin/env python3
"""Test script for the new automatic holiday generation"""

import sys
import os

# Add the parent directory (project root) to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import get_members, COUNTRY_CODE_MAP


def test_member_based_generation():
    print("=== Member-Based Holiday Generation Test ===")

    # Load member data
    members_data = get_members()
    print(f"Total members: {len(members_data)}")
    print()

    # Extract unique countries and regions
    countries_in_use = set()
    regions_in_use = []

    print("Team Members:")
    for member_id, member in members_data.items():
        name = member.get("name", "Unknown")
        country = member.get("country", "")
        region = member.get("region", "")

        print(f"  {name}: {country}" + (f" - {region}" if region else ""))

        if country:
            countries_in_use.add(country)
            if region:
                regions_in_use.append({"country": country, "region": region})

    print()
    print("Holidays will be generated for:")
    print(f"  Countries: {sorted(list(countries_in_use))}")
    print(f"  Regions: {[f'{r['region']} ({r['country']})' for r in regions_in_use]}")

    print()
    print("Country code mapping:")
    for country in countries_in_use:
        code = COUNTRY_CODE_MAP.get(country, "NOT FOUND")
        print(f"  {country} -> {code}")


if __name__ == "__main__":
    test_member_based_generation()
