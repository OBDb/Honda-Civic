#!/usr/bin/env python3
"""
Tool for updating YAML test cases with current signal values.
This is useful when signals are removed from signalsets and tests need to be updated.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Update YAML test expected values based on current signalsets')
    parser.add_argument('--test-cases-dir', default=None, help='Path to test_cases directory')
    parser.add_argument('--year', type=int, action='append', help='Specific model year(s) to update')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    # Find test_cases directory
    if args.test_cases_dir:
        test_cases_dir = args.test_cases_dir
    else:
        # Try to find it relative to current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_cases_dir = os.path.join(script_dir, 'test_cases')

    if not os.path.isdir(test_cases_dir):
        print(f"Error: Test cases directory not found: {test_cases_dir}")
        sys.exit(1)

    print(f"Using test cases directory: {test_cases_dir}")

    # Import our module
    try:
        from schemas.python.yaml_test_updater import update_yaml_tests
        update_yaml_tests(test_cases_dir, args.year, args.dry_run, args.verbose)
    except ImportError as e:
        print(f"Error importing yaml_test_updater module: {e}")
        print("Make sure the schemas package is properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating YAML tests: {e}")
        sys.exit(1)

    print("Done!")

if __name__ == "__main__":
    main()
