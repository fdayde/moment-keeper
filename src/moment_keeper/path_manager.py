"""Gestion des chemins de fichiers cross-platform."""

from pathlib import Path
from typing import Optional


class PathManager:
    """Gestionnaire de chemins pour la compatibilité multi-plateforme."""

    def __init__(self, dossier_base: Optional[Path] = None):
        self.dossier_base = Path(dossier_base) if dossier_base else Path.cwd()

    def obtenir_chemin_absolu(self, chemin_relatif: str) -> Path:
        """Convertit un chemin relatif en chemin absolu."""
        chemin = Path(chemin_relatif)
        if chemin.is_absolute():
            return chemin
        return self.dossier_base / chemin

    def valider_dossier(self, chemin: Path) -> bool:
        """Vérifie qu'un dossier existe et est accessible."""
        return chemin.exists() and chemin.is_dir()

    def creer_dossier_si_necessaire(self, chemin: Path) -> Path:
        """Crée un dossier s'il n'existe pas."""
        chemin.mkdir(parents=True, exist_ok=True)
        return chemin
