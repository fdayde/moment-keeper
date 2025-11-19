"""Module de logging centralisé pour MomentKeeper."""

import logging
import sys
from pathlib import Path


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure et retourne un logger pour un module.

    Args:
        name: Nom du logger (généralement __name__ du module)
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger configuré

    Example:
        >>> from .logger import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info("Message d'information")
    """
    logger = logging.getLogger(name)

    # Ne pas ajouter de handler si le logger en a déjà
    # (évite les messages dupliqués)
    if logger.handlers:
        return logger

    # Configurer le niveau
    logger.setLevel(level)

    # Handler console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Format des messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Ne pas propager au logger parent (évite duplication)
    logger.propagate = False

    return logger


def get_log_file_path() -> Path:
    """Retourne le chemin du fichier de log selon l'OS.

    Returns:
        Path vers le fichier momentkeeper.log dans le dossier approprié
    """
    if sys.platform == "win32":
        import os

        base = Path(os.environ.get("APPDATA", str(Path.home())))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Logs"
    else:
        base = Path.home() / ".local" / "share"

    log_dir = base / "momentkeeper"
    log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir / "momentkeeper.log"


def setup_file_logger(
    name: str, level: int = logging.INFO, enable_file: bool = False
) -> logging.Logger:
    """Configure un logger avec sortie fichier en plus de la console.

    Args:
        name: Nom du logger
        level: Niveau de logging
        enable_file: Active la sauvegarde dans un fichier (désactivé par défaut)

    Returns:
        Logger configuré avec console et optionnellement fichier
    """
    logger = setup_logger(name, level)

    # Ajouter handler fichier si demandé
    if enable_file and not any(
        isinstance(h, logging.FileHandler) for h in logger.handlers
    ):
        log_file = get_log_file_path()

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
