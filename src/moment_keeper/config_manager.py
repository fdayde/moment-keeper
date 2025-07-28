"""Gestionnaire de configuration persistante pour MomentKeeper."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """Gère la sauvegarde et le chargement de la configuration."""

    def __init__(self, config_file: str = "momentkeeper_config.json"):
        """Initialise le gestionnaire de configuration.

        Args:
            config_file: Nom du fichier de configuration
        """
        self.config_file = Path.home() / ".momentkeeper" / config_file
        self.config_file.parent.mkdir(exist_ok=True)

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
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
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
                ).date()

            return config
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
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
            print(f"Erreur lors de la suppression de la configuration: {e}")
            return False
