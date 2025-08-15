#!/usr/bin/env python3
"""Test script to verify holiday generation API"""

import sys
import os

# Add the parent directory (project root) to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import get_supported_regions, COUNTRIES_CONFIG


def test_holiday_generation():
    print("=== Holiday Generation Test ===")
    print(f"Available countries: {list(COUNTRIES_CONFIG.keys())}")
    print()

    for code, data in COUNTRIES_CONFIG.items():
        country_name = data["name"]
        print(f"Testing {country_name} ({code}):")
        regions = get_supported_regions(code)
        print(f"  Available regions: {len(regions)}")
        if regions:
            print(f"  First 3 regions: {regions[:3]}")
        print()

    print("=== API Test Data ===")
    print("Sample JSON for API call:")
    import json

    sample_data = {
        "year": 2025,
        "countries": ["United States", "Australia"],
        "regions": [
            {"country": "United States", "region": "California"},
            {"country": "Australia", "region": "New South Wales"},
        ],
    }
    print(json.dumps(sample_data, indent=2))


if __name__ == "__main__":
    test_holiday_generation()
