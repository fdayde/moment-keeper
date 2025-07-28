"""Module pour les opérations de copie et déplacement de fichiers."""

import shutil
from pathlib import Path


class PhotoCopier:
    """Gestionnaire des opérations sur les fichiers photo."""

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
