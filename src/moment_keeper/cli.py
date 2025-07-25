"""Interface en ligne de commande pour MomentKeeper."""

import argparse
from datetime import datetime
from pathlib import Path

from .organizer import OrganisateurPhotos


def main():
    parser = argparse.ArgumentParser(
        description="MomentKeeper - Organisateur automatique de photos"
    )

    parser.add_argument("dossier_racine", type=str, help="Dossier racine du projet")

    parser.add_argument(
        "date_naissance", type=str, help="Date de naissance (format: YYYY-MM-DD)"
    )

    parser.add_argument(
        "--photos-dir",
        type=str,
        default="photos",
        help="Nom du sous-dossier contenant les photos (défaut: photos)",
    )

    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Simule l'organisation sans déplacer les fichiers",
    )

    parser.add_argument(
        "--reset", action="store_true", help="Remet tous les fichiers à la racine"
    )

    args = parser.parse_args()

    try:
        dossier_racine = Path(args.dossier_racine)
        if not dossier_racine.exists():
            print(f"Erreur: Le dossier racine '{dossier_racine}' n'existe pas")
            return 1

        dossier_photos = dossier_racine / args.photos_dir
        if not dossier_photos.exists():
            print(f"Erreur: Le dossier photos '{dossier_photos}' n'existe pas")
            return 1

        date_naissance = datetime.strptime(args.date_naissance, "%Y-%m-%d")
        organiseur = OrganisateurPhotos(dossier_racine, args.photos_dir, date_naissance)

        if args.reset:
            print("Réinitialisation en cours...")
            nb_fichiers, erreurs = organiseur.reinitialiser()
            print(f"✅ {nb_fichiers} fichiers remis à la racine")

        elif args.simulate:
            print("Simulation de l'organisation...")
            repartition, erreurs = organiseur.simuler_organisation()

            total = sum(len(f) for f in repartition.values())
            print(f"\n📊 {total} photos à organiser:")

            for dossier, fichiers in sorted(repartition.items()):
                print(f"\n📁 {dossier}: {len(fichiers)} photos")
                for fichier in fichiers[:3]:
                    print(f"   - {fichier.name}")
                if len(fichiers) > 3:
                    print(f"   ... et {len(fichiers) - 3} autres")

        else:
            print("Organisation des photos...")
            nb_fichiers, erreurs = organiseur.organiser()
            print(f"✅ {nb_fichiers} photos organisées avec succès!")

        if erreurs:
            print("\n⚠️ Erreurs rencontrées:")
            for erreur in erreurs:
                print(f"   - {erreur}")

        return 0

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
