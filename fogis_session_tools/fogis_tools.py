#!/usr/bin/env python3
"""
Fogis Tools - Unified Interface

A simple text-based menu interface for all Fogis session management tools.

Usage:
    python fogis_tools.py
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
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


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the application header."""
    clear_screen()
    print("=" * 60)
    print("                   FOGIS SESSION TOOLS")
    print("=" * 60)
    print()


def print_menu():
    """Print the main menu options."""
    print("\nPlease select an option:")
    print("1. Login and Save Cookies")
    print("2. Maintain Session (Keep Alive)")
    print("3. Check Session Status")
    print("4. Test Session Timeout")
    print("5. Test Cookie Uniqueness")
    print("6. Exit")
    print()
    return input("Enter your choice (1-6): ")


def get_credentials():
    """Get credentials from .env file or user input."""
    # Try to load from .env file
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        username = os.getenv("FOGIS_USERNAME")
        password = os.getenv("FOGIS_PASSWORD")
        
        if username and password:
            use_env = input(f"Use credentials from .env file for {username}? (y/n): ")
            if use_env.lower() == 'y':
                return username, password
    
    # Get credentials from user input
    username = input("Enter your Fogis username: ")
    password = input("Enter your Fogis password: ")
    
    # Ask if user wants to save to .env
    save_env = input("Save credentials to .env file for future use? (y/n): ")
    if save_env.lower() == 'y':
        with open(".env", "w") as f:
            f.write(f"FOGIS_USERNAME={username}\n")
            f.write(f"FOGIS_PASSWORD={password}\n")
        print("Credentials saved to .env file")
    
    return username, password


def get_cookies_file():
    """Get the path to a cookies file."""
    # Check for existing cookie files
    cookie_files = list(Path(".").glob("fogis_cookies*.json"))
    
    if cookie_files:
        print("\nFound existing cookie files:")
        for i, file in enumerate(cookie_files, 1):
            # Try to get creation time
            try:
                with open(file, 'r') as f:
                    cookies = json.load(f)
                print(f"{i}. {file} (contains {len(cookies)} cookies)")
            except:
                print(f"{i}. {file}")
        
        print(f"{len(cookie_files) + 1}. Create new cookies")
        
        choice = input(f"\nEnter your choice (1-{len(cookie_files) + 1}): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(cookie_files):
                return str(cookie_files[choice - 1])
            elif choice == len(cookie_files) + 1:
                return None
            else:
                print("Invalid choice. Creating new cookies.")
                return None
        except ValueError:
            print("Invalid input. Creating new cookies.")
            return None
    
    return None


def login_and_save_cookies():
    """Login to Fogis and save cookies to a file."""
    print_header()
    print("LOGIN AND SAVE COOKIES")
    print("-" * 60)
    
    username, password = get_credentials()
    
    try:
        print(f"\nLogging in as {username}...")
        client = FogisApiClient(username=username, password=password)
        client.login()
        cookies = client.get_cookies()
        
        if not cookies:
            print("Error: No cookies returned after login")
            return
        
        # Save cookies to file
        filename = f"fogis_cookies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"Login successful! Cookies saved to {filename}")
        print(f"Found {len(cookies)} cookies")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")


def maintain_session():
    """Run the session keeper to maintain a persistent session."""
    print_header()
    print("MAINTAIN SESSION (KEEP ALIVE)")
    print("-" * 60)
    
    cookies_file = get_cookies_file()
    
    if not cookies_file:
        print("\nNo cookies file selected. Please login first.")
        input("\nPress Enter to continue...")
        return
    
    # Get interval
    interval = input("\nEnter check interval in minutes (default: 5): ")
    try:
        interval = int(interval) * 60 if interval else 300
    except ValueError:
        interval = 300
        print("Invalid input. Using default interval of 5 minutes.")
    
    # Get log file
    log_file = input("\nEnter log file path (default: fogis_session.log): ")
    log_file = log_file if log_file else "fogis_session.log"
    
    print("\nStarting session keeper...")
    print(f"Cookies file: {cookies_file}")
    print(f"Interval: {interval // 60} minutes")
    print(f"Log file: {log_file}")
    print("\nSession keeper will run in the background.")
    print("You can check its status using option 3 from the main menu.")
    print("Press Ctrl+C to stop the session keeper.")
    
    try:
        # Build the command
        cmd = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "fogis_session_keeper.py"),
            "--cookies-file", cookies_file,
            "--interval", str(interval),
            "--monitor",
            "--log-file", log_file
        ]
        
        # Run the command
        process = subprocess.Popen(cmd)
        
        print(f"\nSession keeper started with PID {process.pid}")
        print("Waiting 5 seconds to check if it's running properly...")
        
        # Wait a bit to see if the process stays running
        time.sleep(5)
        
        if process.poll() is None:
            print("Session keeper is running successfully!")
        else:
            print("Session keeper stopped unexpectedly.")
            print(f"Exit code: {process.returncode}")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")


def check_session_status():
    """Check the status of a running session keeper."""
    print_header()
    print("CHECK SESSION STATUS")
    print("-" * 60)
    
    status_file = os.path.join(os.path.dirname(__file__), "session_keeper_status.json")
    
    if not os.path.exists(status_file):
        print("\nStatus file not found. Is the session keeper running?")
        input("\nPress Enter to continue...")
        return
    
    try:
        # Read status file
        with open(status_file, 'r') as f:
            status = json.load(f)
        
        # Print status
        print("\n=== Session Keeper Status ===")
        print(f"Running: {status['running']}")
        print(f"Successful checks: {status['successful_checks']}")
        print(f"Failed checks: {status['failed_checks']}")
        print(f"Relogins: {status['relogins']}")
        print(f"Runtime: {status['runtime']}")
        print(f"Last activity: {status['last_activity']}")
        print(f"Check interval: {status['check_interval']} seconds")
        print(f"Has cookies: {status['has_cookies']}")
        
        # Check if the session keeper is still active
        last_activity_parts = status['last_activity'].split()
        if len(last_activity_parts) >= 4 and last_activity_parts[1] == "h":
            hours = int(last_activity_parts[0])
            minutes = int(last_activity_parts[2])
            
            if hours > 0 or minutes > 10:
                print("\nWARNING: Session keeper may be inactive!")
                print(f"Last activity was {status['last_activity']}")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"Error reading status file: {str(e)}")
        input("\nPress Enter to continue...")


def test_session_timeout():
    """Test how long a session remains valid without activity."""
    print_header()
    print("TEST SESSION TIMEOUT")
    print("-" * 60)
    
    cookies_file = get_cookies_file()
    
    if not cookies_file:
        print("\nNo cookies file selected. Please login first.")
        input("\nPress Enter to continue...")
        return
    
    # Ask about adaptive intervals
    use_adaptive = input("\nUse adaptive intervals based on duration? (y/n, default: y): ")
    use_adaptive = use_adaptive.lower() != 'n'
    
    # Get starting interval
    start_interval = input("\nEnter starting interval in minutes (default: 5): ")
    try:
        start_interval = int(start_interval) * 60 if start_interval else 300
    except ValueError:
        start_interval = 300
        print("Invalid input. Using default starting interval of 5 minutes.")
    
    # Get log file
    log_file = input("\nEnter log file path (default: session_timeout_test.log): ")
    log_file = log_file if log_file else "session_timeout_test.log"
    
    print("\nStarting session timeout test...")
    print(f"Cookies file: {cookies_file}")
    print(f"Starting interval: {start_interval // 60} minutes")
    print(f"Adaptive intervals: {use_adaptive}")
    print(f"Log file: {log_file}")
    print("\nThis test will run until the session expires.")
    print("Results will be saved to the log file.")
    print("Press Ctrl+C to stop the test.")
    
    try:
        # Build the command
        cmd = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "auto_test_session_timeout.py"),
            "--cookies-file", cookies_file,
            "--log-file", log_file
        ]
        
        if use_adaptive:
            cmd.append("--adaptive")
        
        # Run the command
        process = subprocess.Popen(cmd)
        
        print(f"\nSession timeout test started with PID {process.pid}")
        print("The test is now running in the background.")
        print(f"You can check the progress in {log_file}")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")


def test_cookie_uniqueness():
    """Test if multiple logins generate unique cookies."""
    print_header()
    print("TEST COOKIE UNIQUENESS")
    print("-" * 60)
    
    username, password = get_credentials()
    
    # Get delay between logins
    delay = input("\nEnter delay between logins in seconds (default: 5): ")
    try:
        delay = int(delay) if delay else 5
    except ValueError:
        delay = 5
        print("Invalid input. Using default delay of 5 seconds.")
    
    print("\nThis test will log in twice and compare the cookies.")
    print("This helps determine if multiple sessions might interfere with each other.")
    print(f"Username: {username}")
    print(f"Delay between logins: {delay} seconds")
    
    try:
        # Build the command
        cmd = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "test_cookie_uniqueness.py"),
            "--username", username,
            "--password", password,
            "--delay", str(delay)
        ]
        
        # Run the command
        process = subprocess.run(cmd, check=True)
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")


def main():
    """Main entry point for the script."""
    while True:
        choice = print_menu()
        
        if choice == '1':
            login_and_save_cookies()
        elif choice == '2':
            maintain_session()
        elif choice == '3':
            check_session_status()
        elif choice == '4':
            test_session_timeout()
        elif choice == '5':
            test_cookie_uniqueness()
        elif choice == '6':
            print("\nExiting Fogis Tools. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Fogis Tools. Goodbye!")
        sys.exit(0)
