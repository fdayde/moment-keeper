#!/usr/bin/env python3
"""Script pour tester les limitations de MomentKeeper."""

import platform

# Ajouter le répertoire parent au path pour les imports
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.moment_keeper.organizer import OrganisateurPhotos  # noqa: E402


def test_filename_patterns():
    """Test des patterns de noms de fichiers supportés."""
    patterns = [
        "20240315_photo.jpg",  # ✅ Format standard
        "20240315_long_description.jpg",  # ✅ Description longue
        "2024-03-15_photo.jpg",  # ❌ Format avec tirets
        "photo_20240315.jpg",  # ❌ Date à la fin
        "20240315.jpg",  # ✅ Date seule
        "IMG_20240315_123456.jpg",  # ❌ Préfixe
        "20240315_été_vacances.jpg",  # ✅ Caractères spéciaux
    ]

    print("Test des patterns de noms de fichiers:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        photos_dir = temp_path / "photos"
        photos_dir.mkdir()

        # Créer les fichiers de test
        for pattern in patterns:
            (photos_dir / pattern).write_bytes(b"test")

        organizer = OrganisateurPhotos(
            dossier_racine=temp_path,
            sous_dossier_photos="photos",
            date_naissance=datetime(2024, 1, 1),
            type_fichiers="photos_only",
        )

        organizer.analyser_photos()

        # Obtenir les résultats de l'analyse
        repartition = organizer.analyser_photos()
        all_processed_files = []
        for files_list in repartition.values():
            all_processed_files.extend([f.name for f in files_list])

        for pattern in patterns:
            if pattern in all_processed_files:
                print(f"   OK {pattern}")
            else:
                print(f"   IGNORE {pattern}")


def test_file_sizes():
    """Test avec différentes tailles de fichiers."""
    sizes = [
        (1024, "1KB"),
        (1024 * 1024, "1MB"),
        (10 * 1024 * 1024, "10MB"),
        (100 * 1024 * 1024, "100MB"),
        (1024 * 1024 * 1024, "1GB"),  # Limite pratique
    ]

    print("\nTest des tailles de fichiers:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        photos_dir = temp_path / "photos"
        photos_dir.mkdir()

        for size_bytes, size_label in sizes:
            filename = f"20240315_test_{size_label.replace('GB', 'G').replace('MB', 'M').replace('KB', 'K')}.jpg"
            filepath = photos_dir / filename

            try:
                # Créer un fichier de la taille demandée
                with open(filepath, "wb") as f:
                    f.write(b"x" * size_bytes)

                organizer = OrganisateurPhotos(
                    dossier_racine=temp_path,
                    sous_dossier_photos="photos",
                    date_naissance=datetime(2024, 1, 1),
                    type_fichiers="photos_only",
                )

                organizer.analyser_photos()
                print(f"   OK {size_label}: Traite avec succes")

            except Exception as e:
                print(f"   ERREUR {size_label}: {str(e)[:50]}...")

            # Nettoyer pour éviter de manquer d'espace disque
            if filepath.exists():
                filepath.unlink()


def test_platform_compatibility():
    """Test de compatibilité multiplateforme."""
    print("\nInformations systeme:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {platform.python_version()}")
    print(f"   Architecture: {platform.machine()}")

    # Test des chemins avec caractères spéciaux
    special_paths = [
        "dossier avec espaces",
        "dossier_avec_accents_ete",
        "dossier-avec-tirets",
        "dossier.avec.points",
    ]

    print("\nTest des chemins speciaux:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for special_name in special_paths:
            try:
                special_dir = temp_path / special_name
                special_dir.mkdir()
                photos_dir = special_dir / "photos"
                photos_dir.mkdir()

                # Créer un fichier de test
                (photos_dir / "20240315_test.jpg").write_bytes(b"test")

                organizer = OrganisateurPhotos(
                    dossier_racine=special_dir,
                    sous_dossier_photos="photos",
                    date_naissance=datetime(2024, 1, 1),
                    type_fichiers="photos_only",
                )

                organizer.analyser_photos()
                print(f"   OK '{special_name}': Compatible")

            except Exception as e:
                print(f"   ERREUR '{special_name}': {str(e)[:50]}...")


def generate_limitations_report():
    """Génère un rapport des limitations."""
    print("\n" + "=" * 60)
    print("RAPPORT DES LIMITATIONS IDENTIFIEES")
    print("=" * 60)

    limitations = [
        "- Format de nom requis: YYYYMMDD_description.ext",
        "- Extensions supportees: .jpg, .jpeg, .png, .heic, .webp (photos)",
        "- Extensions supportees: .mp4, .mov, .avi, .mkv, .m4v, .3gp, .wmv (videos)",
        "- Taille de fichier recommandee: < 1GB pour des performances optimales",
        "- Calcul d'age base sur le nom de fichier uniquement (pas d'EXIF)",
        "- Necessite Python 3.8+ et les dependances listees",
    ]

    for limitation in limitations:
        print(limitation)

    print("\nAMELIORATIONS FUTURES (V2.0):")
    future_features = [
        "- Lecture des donnees EXIF pour extraction automatique des dates",
        "- Support des formats RAW (CR2, NEF, ARW, etc.)",
        "- Organisation par evenements detectes automatiquement",
        "- Interface de renommage en masse",
        "- Synchronisation cloud (Google Photos, iCloud, etc.)",
    ]

    for feature in future_features:
        print(feature)


if __name__ == "__main__":
    test_filename_patterns()
    test_file_sizes()
    test_platform_compatibility()
    generate_limitations_report()
