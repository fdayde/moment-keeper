"""Module principal pour l'organisation des photos."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import EXTENSIONS_PHOTOS, EXTENSIONS_VIDEOS
from .photo_copier import PhotoCopier


class OrganisateurPhotos:
    """Organisateur principal des photos par mois."""

    def __init__(
        self,
        dossier_racine: Path,
        sous_dossier_photos: str,
        date_naissance: datetime,
        type_fichiers: str = "📸🎬 Photos et Vidéos",
    ):
        self.dossier_racine = Path(dossier_racine)
        self.dossier_source = self.dossier_racine / sous_dossier_photos
        self.date_naissance = date_naissance
        self.copieur = PhotoCopier()
        self.type_fichiers = type_fichiers
        self.extensions_actives = self._get_extensions_actives()

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

    def _get_extensions_actives(self) -> set[str]:
        """Retourne les extensions actives selon le type de fichiers sélectionné."""
        if self.type_fichiers == "📸 Photos uniquement":
            return EXTENSIONS_PHOTOS
        elif self.type_fichiers == "🎬 Vidéos uniquement":
            return EXTENSIONS_VIDEOS
        else:  # 📸🎬 Photos et Vidéos
            return EXTENSIONS_PHOTOS | EXTENSIONS_VIDEOS

    def get_file_type(self, filepath: Path) -> str:
        """Retourne 'photo' ou 'video' selon l'extension."""
        extension = filepath.suffix.lower()
        if extension in EXTENSIONS_PHOTOS:
            return "photo"
        elif extension in EXTENSIONS_VIDEOS:
            return "video"
        return "unknown"

    def analyser_photos(self) -> dict[str, list[Path]]:
        """Analyse les photos et retourne la répartition par dossier."""
        repartition = {}
        fichiers_ignores = []

        for fichier in self.dossier_source.iterdir():
            if fichier.is_file() and fichier.suffix.lower() in self.extensions_actives:
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

    def simuler_organisation(self) -> tuple[dict[str, list[Path]], list[str]]:
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

    def organiser(self) -> tuple[int, list[str]]:
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

    def reinitialiser(self) -> tuple[int, list[str]]:
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

    def calculer_taille_fichiers_organises(self, repartition: dict) -> float:
        """Calcule la taille totale des fichiers qui seront organisés en GB."""
        taille_totale = 0
        for fichiers in repartition.values():
            for fichier in fichiers:
                if fichier.exists():
                    taille_totale += fichier.stat().st_size
        return taille_totale / (1024 * 1024 * 1024)  # Convertir en GB
