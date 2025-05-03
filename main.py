#!/usr/bin/env python
"""
Personal Finance Tracker Application

A Python-based personal finance tracker that analyzes spending patterns
and provides budgeting suggestions.
"""
import sys
import os
import argparse
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend by default

from finance_tracker.ui.cli import main as cli_main
# We'll uncomment these when we implement GUI and web interfaces
# from finance_tracker.ui.gui import main as gui_main
from finance_tracker.ui.web import main as web_main


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Personal Finance Tracker")
    
    parser.add_argument(
        "--interface", "-i",
        choices=["cli", "gui", "web"],
        default="cli",
        help="Interface to use (cli, gui, or web)"
    )
    
    parser.add_argument(
        "--db-path",
        help="Path to the database file"
    )
    
    return parser.parse_args()


def main():
    """Application entry point."""
    args = parse_arguments()
    
    # Set database path if provided
    if args.db_path:
        os.environ["FINANCE_DB_PATH"] = args.db_path
    
    # Launch the appropriate interface
    if args.interface == "cli":
        cli_main()
    elif args.interface == "gui":
        print("GUI interface not implemented yet.")
        # gui_main()
    elif args.interface == "web":
        print("Starting web interface...")
        web_main()
    else:
        print(f"Unknown interface: {args.interface}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())