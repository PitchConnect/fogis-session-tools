#!/usr/bin/env python3
"""
Test Fogis Session Timeout Thresholds

This script tests how long a Fogis session remains valid without activity
by gradually increasing the time between validation checks.

Usage:
    python test_session_timeout.py --cookies-file cookies.json [options]

Options:
    --start-interval SECONDS    Starting interval in seconds (default: 300)
    --multiplier FACTOR         Factor to increase interval by each time (default: 1.5)
    --max-interval SECONDS      Maximum interval to test in seconds (default: 86400)
    --log-file FILE             Path to log file (default: session_timeout_test.log)
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the fogis_api_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from fogis_api_client import FogisApiClient
except ImportError:
    print("Error: Could not import FogisApiClient. Make sure the fogis-api-client package is installed.")
    sys.exit(1)


def setup_logging(log_file):
    """Set up logging to both console and file."""
    # Configure logging
    logger = logging.getLogger('session_timeout_test')
    logger.setLevel(logging.INFO)
    logger.handlers = []  # Remove any existing handlers
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


def format_time(seconds):
    """Format seconds into a human-readable time string."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"


def test_session_timeout(cookies_file, start_interval=300, max_interval=86400, multiplier=1.5, log_file="session_timeout_test.log"):
    """
    Test how long a session remains valid without activity.
    
    Args:
        cookies_file: Path to the cookies JSON file
        start_interval: Starting interval in seconds (default: 5 minutes)
        max_interval: Maximum interval to test in seconds (default: 24 hours)
        multiplier: Factor to increase interval by each time (default: 1.5)
        log_file: Path to log file
    """
    logger = setup_logging(log_file)
    
    # Load cookies from file
    try:
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
        logger.info(f"Loaded cookies from {cookies_file}")
    except Exception as e:
        logger.error(f"Error loading cookies: {e}")
        return
    
    # Create client with cookies
    client = FogisApiClient(cookies=cookies)
    
    # Initial validation
    if not client.validate_cookies():
        logger.error("Initial cookie validation failed. Cookies may already be expired.")
        return
    
    logger.info("=" * 60)
    logger.info("Starting session timeout test")
    logger.info(f"Initial interval: {format_time(start_interval)}")
    logger.info(f"Multiplier: {multiplier}")
    logger.info(f"Maximum interval: {format_time(max_interval)}")
    logger.info("=" * 60)
    
    # Test increasingly longer intervals
    current_interval = start_interval
    last_success_time = datetime.now()
    test_number = 1
    
    while current_interval <= max_interval:
        # Calculate and display the next check time
        next_check_time = datetime.now() + timedelta(seconds=current_interval)
        logger.info(f"Test #{test_number}: Waiting for {format_time(current_interval)}")
        logger.info(f"Next check scheduled at: {next_check_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Wait for the specified interval
        time.sleep(current_interval)
        
        # Try to validate cookies
        try:
            current_time = datetime.now()
            elapsed = (current_time - last_success_time).total_seconds()
            
            if client.validate_cookies():
                logger.info(f"✅ SUCCESS: Session still valid after {format_time(elapsed)} of inactivity")
                last_success_time = current_time
                
                # Increase interval for next test
                previous_interval = current_interval
                current_interval = min(current_interval * multiplier, max_interval)
                logger.info(f"Increasing interval from {format_time(previous_interval)} to {format_time(current_interval)}")
                test_number += 1
            else:
                logger.info(f"❌ EXPIRED: Session expired after {format_time(elapsed)} of inactivity")
                logger.info(f"Last successful interval: {format_time(current_interval / multiplier)}")
                break
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            elapsed = (datetime.now() - last_success_time).total_seconds()
            logger.info(f"❌ ERROR: Session check failed after {format_time(elapsed)} of inactivity")
            break
    
    logger.info("=" * 60)
    logger.info("Session timeout test completed")
    logger.info("=" * 60)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Test Fogis session timeout thresholds")
    parser.add_argument("--cookies-file", required=True, help="Path to cookies JSON file")
    parser.add_argument("--start-interval", type=int, default=300, 
                        help="Starting interval in seconds (default: 300)")
    parser.add_argument("--max-interval", type=int, default=86400, 
                        help="Maximum interval to test in seconds (default: 86400)")
    parser.add_argument("--multiplier", type=float, default=1.5, 
                        help="Factor to increase interval by each time (default: 1.5)")
    parser.add_argument("--log-file", default="session_timeout_test.log",
                        help="Path to log file (default: session_timeout_test.log)")
    
    args = parser.parse_args()
    
    try:
        test_session_timeout(
            args.cookies_file,
            args.start_interval,
            args.max_interval,
            args.multiplier,
            args.log_file
        )
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
