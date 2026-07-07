"""
CLI launcher for MomentKeeper.

This module provides a simple command-line interface that launches
the Streamlit web interface.
"""

import subprocess
import sys
from pathlib import Path

from .logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Launch the MomentKeeper Streamlit application."""
    # Get the path to app.py relative to this file
    current_dir = Path(__file__).parent.parent.parent
    app_path = current_dir / "app.py"

    if not app_path.exists():
        logger.error(f"Could not find app.py at {app_path}")
        sys.exit(1)

    logger.info("Starting MomentKeeper...")
    logger.info(f"Launching Streamlit app from: {app_path}")

    try:
        # Launch streamlit via the current Python interpreter (works even if
        # streamlit n'est pas sur le PATH, ex. dans un venv non activé)
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error launching Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("MomentKeeper closed by user")
        sys.exit(0)
    except FileNotFoundError:
        logger.error(
            "Streamlit is not installed. Please install it with: pip install streamlit"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
