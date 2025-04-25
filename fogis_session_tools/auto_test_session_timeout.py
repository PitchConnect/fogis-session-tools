#!/usr/bin/env python3
"""
Automated Session Timeout Testing

This script automates the entire process of testing session timeouts:
1. Reads credentials from .env file
2. Logs in and gets fresh cookies
3. Tests session timeout with adaptive intervals
4. Provides detailed results

Usage:
    python auto_test_session_timeout.py [options]

Options:
    --env-file FILE             Path to .env file (default: .env)
    --adaptive                  Use adaptive intervals based on duration
    --log-file FILE             Path to log file (default: session_timeout_test.log)
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add the parent directory to the path so we can import the fogis_api_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from fogis_api_client import FogisApiClient
    from dotenv import load_dotenv
except ImportError:
    print("Error: Missing dependencies. Please install them with:")
    print("pip install fogis-api-client python-dotenv")
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


def get_adaptive_interval(current_interval, elapsed_time):
    """
    Get the next interval using an adaptive strategy based on elapsed time.
    
    Args:
        current_interval: Current interval in seconds
        elapsed_time: Total elapsed time so far in seconds
        
    Returns:
        next_interval: Next interval to test in seconds
    """
    # For short durations (< 1 hour): Use smaller increments
    if elapsed_time < 3600:
        return current_interval * 1.5
    
    # For medium durations (1-3 hours): Use medium increments
    elif elapsed_time < 10800:
        # If current interval is less than 30 minutes, jump to 30 minutes
        if current_interval < 1800:
            return 1800
        # Otherwise use 30-minute increments
        return current_interval + 1800
    
    # For long durations (> 3 hours): Use larger increments
    else:
        # If current interval is less than 1 hour, jump to 1 hour
        if current_interval < 3600:
            return 3600
        # Otherwise use 1-hour increments
        return current_interval + 3600


def test_session_timeout(client, use_adaptive=False, max_interval=86400, log_file="session_timeout_test.log"):
    """
    Test how long a session remains valid without activity.
    
    Args:
        client: Authenticated FogisApiClient instance
        use_adaptive: Whether to use adaptive intervals
        max_interval: Maximum interval to test in seconds (default: 24 hours)
        log_file: Path to log file
    """
    logger = setup_logging(log_file)
    
    # Initial validation
    if not client.validate_cookies():
        logger.error("Initial cookie validation failed. Cookies may already be expired.")
        return
    
    logger.info("=" * 60)
    logger.info("Starting session timeout test")
    logger.info(f"Adaptive intervals: {use_adaptive}")
    logger.info(f"Maximum interval: {format_time(max_interval)}")
    logger.info("=" * 60)
    
    # Start with a 5-minute interval
    current_interval = 300
    last_success_time = datetime.now()
    test_start_time = datetime.now()
    test_number = 1
    total_elapsed = 0
    
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
            total_elapsed = (current_time - test_start_time).total_seconds()
            
            if client.validate_cookies():
                logger.info(f"✅ SUCCESS: Session still valid after {format_time(elapsed)} of inactivity")
                logger.info(f"Total test duration so far: {format_time(total_elapsed)}")
                last_success_time = current_time
                
                # Determine next interval
                previous_interval = current_interval
                if use_adaptive:
                    current_interval = min(get_adaptive_interval(current_interval, total_elapsed), max_interval)
                    logger.info(f"Using adaptive strategy: {format_time(previous_interval)} → {format_time(current_interval)}")
                else:
                    current_interval = min(current_interval * 1.5, max_interval)
                    logger.info(f"Increasing by factor of 1.5: {format_time(previous_interval)} → {format_time(current_interval)}")
                
                test_number += 1
            else:
                logger.info(f"❌ EXPIRED: Session expired after {format_time(elapsed)} of inactivity")
                logger.info(f"Last successful interval: {format_time(current_interval / (1.5 if not use_adaptive else 1.2))}")
                logger.info(f"Total test duration: {format_time(total_elapsed)}")
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
    parser = argparse.ArgumentParser(description="Automated Fogis session timeout testing")
    parser.add_argument("--env-file", default=".env", help="Path to .env file (default: .env)")
    parser.add_argument("--adaptive", action="store_true", help="Use adaptive intervals based on duration")
    parser.add_argument("--max-interval", type=int, default=86400, 
                        help="Maximum interval to test in seconds (default: 86400)")
    parser.add_argument("--log-file", default="session_timeout_test.log",
                        help="Path to log file (default: session_timeout_test.log)")
    parser.add_argument("--cookies-file", help="Path to existing cookies file (optional)")
    
    args = parser.parse_args()
    
    try:
        # Set up client
        client = None
        
        # If cookies file is provided, use it
        if args.cookies_file:
            try:
                with open(args.cookies_file, 'r') as f:
                    cookies = json.load(f)
                client = FogisApiClient(cookies=cookies)
                print(f"Using cookies from {args.cookies_file}")
            except Exception as e:
                print(f"Error loading cookies: {e}")
                return 1
        
        # Otherwise, use credentials from .env
        else:
            # Load environment variables
            env_path = Path(args.env_file)
            if not env_path.exists():
                print(f"Error: .env file not found at {env_path}")
                print("Please create a .env file with FOGIS_USERNAME and FOGIS_PASSWORD")
                return 1
                
            load_dotenv(dotenv_path=env_path)
            
            username = os.getenv("FOGIS_USERNAME")
            password = os.getenv("FOGIS_PASSWORD")
            
            if not username or not password:
                print("Error: FOGIS_USERNAME and FOGIS_PASSWORD must be set in .env file")
                return 1
                
            # Create client and login
            client = FogisApiClient(username=username, password=password)
            print(f"Logging in as {username}...")
            client.login()
            print("Login successful")
            
            # Save cookies for future use
            cookies = client.get_cookies()
            with open("fogis_cookies.json", 'w') as f:
                json.dump(cookies, f, indent=2)
            print("Cookies saved to fogis_cookies.json")
        
        # Run the test
        test_session_timeout(
            client,
            use_adaptive=args.adaptive,
            max_interval=args.max_interval,
            log_file=args.log_file
        )
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
