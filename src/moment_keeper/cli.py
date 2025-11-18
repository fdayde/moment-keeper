"""
CLI launcher for MomentKeeper.

This module provides a simple command-line interface that launches
the Streamlit web interface.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the MomentKeeper Streamlit application."""
    # Get the path to app.py relative to this file
    current_dir = Path(__file__).parent.parent.parent
    app_path = current_dir / "app.py"

    if not app_path.exists():
        print(f"Error: Could not find app.py at {app_path}", file=sys.stderr)
        sys.exit(1)

    print("🦖 Starting MomentKeeper...")
    print(f"   Launching Streamlit app from: {app_path}")
    print()

    try:
        # Launch streamlit with the app.py file
        subprocess.run(
            ["streamlit", "run", str(app_path)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 MomentKeeper closed.")
        sys.exit(0)
    except FileNotFoundError:
        print(
            "Error: Streamlit is not installed. Please install it with:",
            file=sys.stderr,
        )
        print("  pip install streamlit", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
