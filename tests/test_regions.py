#!/usr/bin/env python3
"""Test script to verify dynamic region detection"""

import sys
import os

# Add the parent directory (project root) to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import get_supported_regions, generate_regions_map, COUNTRIES_CONFIG


def test_region_detection():
    print("=== Dynamic Region Detection Test ===")
    print(f"Countries in config: {list(COUNTRIES_CONFIG.keys())}")
    print()

    for code, data in COUNTRIES_CONFIG.items():
        country_name = data["name"]
        print(f"Testing {country_name} ({code}):")
        regions = get_supported_regions(code)
        print(f"  Found {len(regions)} regions: {regions[:5]}{'...' if len(regions) > 5 else ''}")
        print()

    print("=== Generated REGIONS_MAP ===")
    regions_map = generate_regions_map()
    for country, regions in regions_map.items():
        print(f"{country}: {len(regions)} regions - {regions[:3]}{'...' if len(regions) > 3 else ''}")


if __name__ == "__main__":
    test_region_detection()
