"""
Hypr-Welcome CLI Entry Point
"""

import sys
import os
import argparse

ONBOARDED_FLAG = os.path.expanduser("~/.local/state/hypr-welcome/.onboarded")

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

    try:
        from .app import run_app
        run_app()
    except (ImportError, ValueError) as e:
        print(f"Error: PyGObject (GTK 3) is required to run the GUI: {e}", file=sys.stderr)
        print("Please install: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
