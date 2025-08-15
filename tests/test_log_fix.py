#!/usr/bin/env python3
"""Test script to verify the log_operation fix"""

import sys
import os

# Add the parent directory (project root) to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Change to src directory to find the data files
os.chdir("src")

from app import log_operation


def test_log_operation_fix():
    print("=== Testing log_operation Fix ===")

    try:
        # Test the log_operation function with the correct parameters
        log_operation(
            "GENERATE_HOLIDAYS",
            None,  # No specific member_id for this system operation
            "Generated 25 holidays for countries: Australia, United States and regions: New South Wales (Australia), California (United States)",
            "System",
        )
        print("✅ log_operation call successful!")

    except Exception as e:
        print(f"❌ log_operation call failed: {e}")

    print("\nTesting with different parameter combinations:")

    # Test with member_id
    try:
        log_operation("TEST_OPERATION", "123", "Test details", "Test User")
        print("✅ log_operation with member_id successful!")
    except Exception as e:
        print(f"❌ log_operation with member_id failed: {e}")

    # Test with minimal parameters (member_name is optional)
    try:
        log_operation("TEST_OPERATION_2", None, "Test details without member name")
        print("✅ log_operation without member_name successful!")
    except Exception as e:
        print(f"❌ log_operation without member_name failed: {e}")


if __name__ == "__main__":
    test_log_operation_fix()
