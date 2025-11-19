"""Gestionnaire de configuration persistante pour MomentKeeper."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .logger import setup_logger

logger = setup_logger(__name__)


class ConfigManager:
    """Gère la sauvegarde et le chargement de la configuration."""

    def __init__(self, config_file: str = "momentkeeper_config.json"):
        """Initialise le gestionnaire de configuration.

        La configuration est stockée dans l'emplacement système approprié :
        - Windows: %APPDATA%/momentkeeper/
        - macOS: ~/Library/Application Support/momentkeeper/
        - Linux: ~/.config/momentkeeper/

        En développement, vérifie d'abord un fichier local dans data/user-config/
        pour faciliter le développement.

        Args:
            config_file: Nom du fichier de configuration
        """
        # Priorité 1 : Config locale (développement seulement)
        local_config = self._get_local_config_path() / config_file

        # Priorité 2 : Config système (production)
        system_config = self._get_system_config_path() / config_file

        # Utiliser config locale si elle existe (dev), sinon système (prod/exe)
        if local_config.exists() and not getattr(sys, "frozen", False):
            self.config_file = local_config
        else:
            self.config_file = system_config
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_local_config_path(self) -> Path:
        """Retourne le chemin de configuration local (développement).

        Returns:
            Path vers data/user-config/ dans le repo (dev uniquement)
        """
        if getattr(sys, "frozen", False):
            # En exécutable, pas de config locale
            return Path()
        try:
            # En développement, dans le repo
            return Path(__file__).parent.parent.parent / "data" / "user-config"
        except Exception:
            return Path()

    def _get_system_config_path(self) -> Path:
        """Retourne le chemin de configuration système selon l'OS.

        Returns:
            Path vers le dossier de config système approprié
        """
        if sys.platform == "win32":
            # Windows: %APPDATA%/momentkeeper/
            base = Path(os.environ.get("APPDATA", str(Path.home())))
        elif sys.platform == "darwin":
            # macOS: ~/Library/Application Support/momentkeeper/
            base = Path.home() / "Library" / "Application Support"
        else:
            # Linux/Unix: ~/.config/momentkeeper/
            base = Path.home() / ".config"

        return base / "momentkeeper"

    def save_config(self, config: dict[str, Any]) -> bool:
        """Sauvegarde la configuration dans un fichier JSON.

        Args:
            config: Dictionnaire de configuration à sauvegarder

        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        try:
            # Convertir les dates en chaînes pour JSON
            config_to_save = config.copy()
            if "date_naissance" in config_to_save and isinstance(
                config_to_save["date_naissance"], datetime
            ):
                config_to_save["date_naissance"] = config_to_save[
                    "date_naissance"
                ].isoformat()

            # Sauvegarder dans le fichier
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            logger.error(
                f"Erreur lors de la sauvegarde de la configuration: {e}", exc_info=True
            )
            return False

    def load_config(self) -> Optional[dict[str, Any]]:
        """Charge la configuration depuis le fichier JSON.

        Returns:
            Dictionnaire de configuration ou None si le fichier n'existe pas
        """
        try:
            if not self.config_file.exists():
                return None

            with open(self.config_file, encoding="utf-8") as f:
                config = json.load(f)

            # Convertir les dates ISO en objets datetime
            if "date_naissance" in config and isinstance(config["date_naissance"], str):
                config["date_naissance"] = datetime.fromisoformat(
                    config["date_naissance"]
                )

            return config
        except Exception as e:
            logger.error(
                f"Erreur lors du chargement de la configuration: {e}", exc_info=True
            )
            return None

    def delete_config(self) -> bool:
        """Supprime le fichier de configuration.

        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except Exception as e:
            logger.error(
                f"Erreur lors de la suppression de la configuration: {e}", exc_info=True
            )
            return False
