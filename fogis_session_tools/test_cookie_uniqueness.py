#!/usr/bin/env python3
"""
Test Cookie Uniqueness

This script tests whether logging in multiple times generates unique cookies.
This is important to know if multiple sessions might interfere with each other.

Usage:
    python test_cookie_uniqueness.py --username USERNAME --password PASSWORD
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

# Add the parent directory to the path so we can import the fogis_api_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from fogis_api_client import FogisApiClient
except ImportError:
    print("Error: Could not import FogisApiClient. Make sure the fogis-api-client package is installed.")
    sys.exit(1)


def compare_cookies(cookies1, cookies2):
    """Compare two sets of cookies and report differences."""
    print("\n=== Cookie Comparison ===")
    
    # Check if the sets of keys are the same
    keys1 = set(cookies1.keys())
    keys2 = set(cookies2.keys())
    
    if keys1 != keys2:
        print("Different cookie keys found:")
        print(f"  Only in first login: {keys1 - keys2}")
        print(f"  Only in second login: {keys2 - keys1}")
    
    # Compare values for common keys
    common_keys = keys1.intersection(keys2)
    different_values = []
    same_values = []
    
    for key in common_keys:
        if cookies1[key] == cookies2[key]:
            same_values.append(key)
        else:
            different_values.append(key)
    
    if different_values:
        print("\nCookies with different values:")
        for key in different_values:
            print(f"  {key}:")
            print(f"    Login 1: {cookies1[key]}")
            print(f"    Login 2: {cookies2[key]}")
    
    if same_values:
        print("\nCookies with identical values:")
        for key in same_values:
            print(f"  {key}: {cookies1[key]}")
    
    # Overall assessment
    if different_values:
        print("\n✅ RESULT: Logins generate different cookies. Multiple sessions should not interfere.")
    else:
        print("\n⚠️ RESULT: Logins generate identical cookies. Multiple sessions may interfere with each other.")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Test if multiple logins generate unique cookies")
    parser.add_argument("--username", required=True, help="Fogis username")
    parser.add_argument("--password", required=True, help="Fogis password")
    parser.add_argument("--delay", type=int, default=5, help="Delay between logins in seconds (default: 5)")
    
    args = parser.parse_args()
    
    try:
        # First login
        print(f"Performing first login as {args.username}...")
        client1 = FogisApiClient(username=args.username, password=args.password)
        client1.login()
        cookies1 = client1.get_cookies()
        print(f"First login successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save first cookies
        with open("fogis_cookies_1.json", 'w') as f:
            json.dump(cookies1, f, indent=2)
        print("First cookies saved to fogis_cookies_1.json")
        
        # Wait before second login
        print(f"Waiting {args.delay} seconds before second login...")
        time.sleep(args.delay)
        
        # Second login
        print(f"Performing second login as {args.username}...")
        client2 = FogisApiClient(username=args.username, password=args.password)
        client2.login()
        cookies2 = client2.get_cookies()
        print(f"Second login successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save second cookies
        with open("fogis_cookies_2.json", 'w') as f:
            json.dump(cookies2, f, indent=2)
        print("Second cookies saved to fogis_cookies_2.json")
        
        # Compare cookies
        compare_cookies(cookies1, cookies2)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
