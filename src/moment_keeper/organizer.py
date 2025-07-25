"""Module principal pour l'organisation des photos."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .path_manager import PathManager
from .photo_copier import PhotoCopier


class OrganisateurPhotos:
    """Organisateur principal des photos par mois."""

    def __init__(
        self, dossier_racine: Path, sous_dossier_photos: str, date_naissance: datetime
    ):
        self.dossier_racine = Path(dossier_racine)
        self.dossier_source = self.dossier_racine / sous_dossier_photos
        self.date_naissance = date_naissance
        self.path_manager = PathManager(self.dossier_racine)
        self.copieur = PhotoCopier()

    def extraire_date_nom_fichier(self, nom_fichier: str) -> Optional[datetime]:
        """Extrait la date du nom de fichier au format YYYYMMDD."""
        try:
            date_str = nom_fichier.split("_")[0]
            if len(date_str) == 8 and date_str.isdigit():
                return datetime.strptime(date_str, "%Y%m%d")
        except (ValueError, IndexError):
            pass
        return None

    def calculer_age_mois(self, date_photo: datetime) -> int:
        """Calcule l'âge en mois à la date de la photo."""
        # Calcul basé sur les mois calendaires
        mois = (date_photo.year - self.date_naissance.year) * 12
        mois += date_photo.month - self.date_naissance.month

        # Ajuster si le jour du mois n'est pas encore atteint
        if date_photo.day < self.date_naissance.day:
            mois -= 1

        return max(0, mois)

    def obtenir_nom_dossier_mois(self, age_mois: int) -> str:
        """Retourne le nom du dossier pour un âge donné."""
        return f"{age_mois}-{age_mois + 1}months"

    def analyser_photos(self) -> Dict[str, List[Path]]:
        """Analyse les photos et retourne la répartition par dossier."""
        repartition = {}
        fichiers_ignores = []

        for fichier in self.dossier_source.iterdir():
            if fichier.is_file() and fichier.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
            ]:
                date_photo = self.extraire_date_nom_fichier(fichier.name)

                if date_photo and date_photo >= self.date_naissance:
                    age_mois = self.calculer_age_mois(date_photo)
                    nom_dossier = self.obtenir_nom_dossier_mois(age_mois)

                    if nom_dossier not in repartition:
                        repartition[nom_dossier] = []
                    repartition[nom_dossier].append(fichier)
                elif date_photo and date_photo < self.date_naissance:
                    fichiers_ignores.append(
                        (fichier.name, "Photo antérieure à la naissance")
                    )
                elif not date_photo:
                    fichiers_ignores.append(
                        (fichier.name, "Format de date non reconnu")
                    )

        # Stocker les fichiers ignorés pour le débogage
        self._fichiers_ignores = fichiers_ignores

        return repartition

    def simuler_organisation(self) -> Tuple[Dict[str, List[Path]], List[str]]:
        """Simule l'organisation sans déplacer les fichiers."""
        repartition = self.analyser_photos()
        erreurs = []

        for nom_dossier, fichiers in repartition.items():
            dossier_cible = self.dossier_racine / nom_dossier
            for fichier in fichiers:
                fichier_cible = dossier_cible / fichier.name
                if fichier_cible.exists():
                    erreurs.append(f"Le fichier {fichier_cible} existe déjà")

        return repartition, erreurs

    def organiser(self) -> Tuple[int, List[str]]:
        """Organise réellement les photos."""
        repartition = self.analyser_photos()
        compteur = 0
        erreurs = []

        for nom_dossier, fichiers in repartition.items():
            dossier_cible = self.dossier_racine / nom_dossier
            dossier_cible.mkdir(exist_ok=True)

            for fichier in fichiers:
                try:
                    self.copieur.deplacer_fichier(fichier, dossier_cible)
                    compteur += 1
                except Exception as e:
                    erreurs.append(f"Erreur pour {fichier.name}: {str(e)}")

        return compteur, erreurs

    def reinitialiser(self) -> Tuple[int, List[str]]:
        """Remet tous les fichiers à la racine."""
        compteur = 0
        erreurs = []

        for dossier in self.dossier_racine.iterdir():
            if dossier.is_dir() and "-" in dossier.name and "month" in dossier.name:
                for fichier in dossier.iterdir():
                    if fichier.is_file():
                        try:
                            self.copieur.deplacer_fichier(fichier, self.dossier_source)
                            compteur += 1
                        except Exception as e:
                            erreurs.append(f"Erreur pour {fichier.name}: {str(e)}")

                if not any(dossier.iterdir()):
                    dossier.rmdir()

        return compteur, erreurs
