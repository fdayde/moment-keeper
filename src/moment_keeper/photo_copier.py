"""Module pour les opérations de copie et déplacement de fichiers."""

import shutil
from pathlib import Path


class PhotoCopier:
    """Gestionnaire des opérations sur les fichiers photo."""

    def deplacer_fichier(self, source: Path, destination_dir: Path) -> Path:
        """Déplace un fichier vers un dossier de destination.

        Args:
            source: Chemin du fichier source
            destination_dir: Dossier de destination

        Returns:
            Path du fichier déplacé

        Raises:
            FileNotFoundError: Si le fichier source n'existe pas
            FileExistsError: Si un fichier avec le même nom existe déjà
            ValueError: Si le chemin de destination est invalide (path traversal)
        """
        if not source.exists():
            raise FileNotFoundError(f"Le fichier source {source} n'existe pas")

        if not destination_dir.exists():
            destination_dir.mkdir(parents=True, exist_ok=True)

        # Construire le chemin de destination
        destination = destination_dir / source.name

        # SÉCURITÉ: Valider que la destination reste dans le dossier autorisé
        # Protection contre les attaques de type path traversal (../../etc/passwd)
        try:
            destination_resolved = destination.resolve()
            destination_dir_resolved = destination_dir.resolve()

            if not destination_resolved.is_relative_to(destination_dir_resolved):
                raise ValueError(
                    f"Destination invalide: tentative de path traversal détectée. "
                    f"Le fichier '{source.name}' tente d'écrire en dehors du dossier autorisé."
                )
        except (ValueError, OSError) as e:
            raise ValueError(f"Chemin de destination invalide: {e}") from e

        if destination.exists():
            raise FileExistsError(f"Le fichier {destination} existe déjà")

        shutil.move(str(source), str(destination))
        return destination

    def copier_fichier(self, source: Path, destination_dir: Path) -> Path:
        """Copie un fichier vers un dossier de destination.

        Args:
            source: Chemin du fichier source
            destination_dir: Dossier de destination

        Returns:
            Path du fichier copié

        Raises:
            FileNotFoundError: Si le fichier source n'existe pas
            FileExistsError: Si un fichier avec le même nom existe déjà
            ValueError: Si le chemin de destination est invalide (path traversal)
        """
        if not source.exists():
            raise FileNotFoundError(f"Le fichier source {source} n'existe pas")

        if not destination_dir.exists():
            destination_dir.mkdir(parents=True, exist_ok=True)

        # Construire le chemin de destination
        destination = destination_dir / source.name

        # SÉCURITÉ: Valider que la destination reste dans le dossier autorisé
        try:
            destination_resolved = destination.resolve()
            destination_dir_resolved = destination_dir.resolve()

            if not destination_resolved.is_relative_to(destination_dir_resolved):
                raise ValueError(
                    f"Destination invalide: tentative de path traversal détectée. "
                    f"Le fichier '{source.name}' tente d'écrire en dehors du dossier autorisé."
                )
        except (ValueError, OSError) as e:
            raise ValueError(f"Chemin de destination invalide: {e}") from e

        if destination.exists():
            raise FileExistsError(f"Le fichier {destination} existe déjà")

        shutil.copy2(str(source), str(destination))
        return destination
