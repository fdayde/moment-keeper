"""Module pour les opérations de copie et déplacement de fichiers."""

import shutil
from pathlib import Path
from typing import Optional


class PhotoCopier:
    """Gestionnaire des opérations sur les fichiers photo."""

    def __init__(self):
        self.historique_deplacements = []

    def deplacer_fichier(self, source: Path, destination_dir: Path) -> Path:
        """Déplace un fichier vers un dossier de destination."""
        if not source.exists():
            raise FileNotFoundError(f"Le fichier source {source} n'existe pas")

        if not destination_dir.exists():
            destination_dir.mkdir(parents=True, exist_ok=True)

        destination = destination_dir / source.name

        if destination.exists():
            raise FileExistsError(f"Le fichier {destination} existe déjà")

        shutil.move(str(source), str(destination))
        self.historique_deplacements.append((source, destination))

        return destination

    def copier_fichier(self, source: Path, destination_dir: Path) -> Path:
        """Copie un fichier vers un dossier de destination."""
        if not source.exists():
            raise FileNotFoundError(f"Le fichier source {source} n'existe pas")

        if not destination_dir.exists():
            destination_dir.mkdir(parents=True, exist_ok=True)

        destination = destination_dir / source.name

        if destination.exists():
            raise FileExistsError(f"Le fichier {destination} existe déjà")

        shutil.copy2(str(source), str(destination))

        return destination

    def annuler_dernier_deplacement(self) -> Optional[tuple]:
        """Annule le dernier déplacement effectué."""
        if not self.historique_deplacements:
            return None

        source_orig, destination = self.historique_deplacements.pop()

        if destination.exists():
            shutil.move(str(destination), str(source_orig))
            return (destination, source_orig)

        return None
