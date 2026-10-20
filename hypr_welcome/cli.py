"""
Hypr-Welcome CLI Entry Point
"""

import sys
import os
import argparse
from .app import run_app, ONBOARDED_FLAG

def main():
    parser = argparse.ArgumentParser(
        prog="hypr-welcome",
        description="First-Boot Onboarding Guide & Hardware Diagnostics for Hyprland"
    )
    parser.add_argument("--first-boot-only", action="store_true", help="Only launch if ~/.local/state/hypr-welcome/.onboarded does not exist")
    parser.add_argument("--reset", action="store_true", help="Reset onboarding state flag")
    args = parser.parse_args()

    if args.reset:
        if os.path.exists(ONBOARDED_FLAG):
            os.remove(ONBOARDED_FLAG)
            print("✓ Reset onboarding state flag.")
        else:
            print("Already in un-onboarded state.")
        sys.exit(0)

    if args.first_boot_only and os.path.exists(ONBOARDED_FLAG):
        # Already onboarded; exit quietly
        sys.exit(0)

    run_app()

if __name__ == "__main__":
    main()
