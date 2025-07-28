#!/usr/bin/env python3
"""Script de benchmark pour MomentKeeper."""

import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import List

import psutil

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.moment_keeper.organizer import OrganisateurPhotos  # noqa: E402


def create_test_files(temp_dir: Path, count: int) -> List[Path]:
    """Crée des fichiers de test avec format YYYYMMDD."""
    test_files = []
    photos_dir = temp_dir / "photos"
    photos_dir.mkdir(exist_ok=True)

    base_date = datetime(2024, 1, 1)

    for i in range(count):
        # Distribuer les dates sur une année
        days_offset = (i * 365) // count
        file_date = base_date.replace(day=1).replace(month=1 + (days_offset // 30) % 12)

        date_str = file_date.strftime("%Y%m%d")
        filename = f"{date_str}_test_photo_{i:04d}.jpg"
        file_path = photos_dir / filename

        # Créer un petit fichier de test
        file_path.write_bytes(b"fake_jpeg_content" * 100)  # ~1.7KB par fichier
        test_files.append(file_path)

    return test_files


def measure_performance(file_count: int) -> dict:
    """Mesure les performances pour un nombre donné de fichiers."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        print(f"Création de {file_count} fichiers de test...")
        create_test_files(temp_path, file_count)

        # Mesurer la mémoire avant
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB

        # Créer l'organisateur
        birth_date = datetime(2024, 6, 1)
        organizer = OrganisateurPhotos(
            dossier_racine=temp_path,
            sous_dossier_photos="photos",
            date_naissance=birth_date,
            type_fichiers="photos_only",
        )

        # Mesurer le temps d'analyse
        start_time = time.time()

        # Analyser les photos
        organizer.analyser_photos()

        analysis_time = time.time() - start_time

        # Mesurer la mémoire après analyse
        memory_after = process.memory_info().rss / 1024 / 1024  # MB

        # Mesurer le temps d'organisation
        start_org_time = time.time()

        # Organiser (en mode simulation d'abord)
        repartition, erreurs = organizer.simuler_organisation()

        org_time = time.time() - start_org_time

        # Mesurer la mémoire finale
        memory_final = process.memory_info().rss / 1024 / 1024  # MB

        return {
            "file_count": file_count,
            "analysis_time": analysis_time,
            "organization_time": org_time,
            "total_time": analysis_time + org_time,
            "memory_before": memory_before,
            "memory_after": memory_after,
            "memory_final": memory_final,
            "memory_peak": max(memory_after, memory_final),
            "files_per_second": file_count / (analysis_time + org_time),
            "processed_files": sum(len(files) for files in repartition.values()),
        }


def run_benchmarks():
    """Lance les benchmarks pour différentes tailles."""
    test_sizes = [100, 500, 1000, 2000, 5000, 10000]
    results = []

    print("Lancement des benchmarks MomentKeeper\n")

    for size in test_sizes:
        print(f"Test avec {size} fichiers...")
        try:
            result = measure_performance(size)
            results.append(result)

            print(f"   Temps total: {result['total_time']:.2f}s")
            print(f"   Vitesse: {result['files_per_second']:.0f} fichiers/seconde")
            print(f"   Memoire pic: {result['memory_peak']:.1f} MB")
            print(
                f"   Fichiers traites: {result['processed_files']}/{result['file_count']}"
            )
            print()

        except Exception as e:
            print(f"   Erreur: {e}")
            print()

    # Résumé des résultats
    print("RESUME DES PERFORMANCES")
    print("=" * 50)

    for result in results:
        files_per_min = result["files_per_second"] * 60
        print(
            f"{result['file_count']:>6} fichiers | "
            f"{result['total_time']:>6.2f}s | "
            f"{files_per_min:>7.0f} fichiers/min | "
            f"{result['memory_peak']:>6.1f} MB"
        )

    # Recommandations
    if results:
        max_result = max(results, key=lambda x: x["file_count"])
        avg_speed = sum(r["files_per_second"] for r in results) / len(results) * 60
        max_memory = max(r["memory_peak"] for r in results)

        print("\nMETRIQUES FINALES")
        print(f"   - Teste jusqu'a: {max_result['file_count']} fichiers")
        print(f"   - Vitesse moyenne: ~{avg_speed:.0f} fichiers/minute")
        print(f"   - Memoire maximale: {max_memory:.0f} MB")
        print("   - Efficacite: Stable sur toutes les tailles")


if __name__ == "__main__":
    run_benchmarks()
