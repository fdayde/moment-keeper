"""Tests unitaires pour le module organizer."""

from datetime import datetime
from pathlib import Path

from moment_keeper.organizer import OrganisateurPhotos


class TestOrganisateurPhotos:
    """Tests pour la classe OrganisateurPhotos."""

    def test_init(self, organiseur):
        """Test l'initialisation de l'organiseur."""
        assert organiseur.dossier_racine.exists()
        assert organiseur.dossier_source.exists()
        assert organiseur.date_naissance == datetime(2024, 6, 1)
        assert organiseur.type_fichiers == "photos"

    def test_analyser_photos(self, organiseur):
        """Test l'analyse des photos."""
        resultats = organiseur.analyser_photos()

        # Vérifier qu'on a bien 4 photos
        assert sum(len(photos) for photos in resultats.values()) == 4

        # Vérifier la répartition par dossier
        assert "1-2months" in resultats
        assert len(resultats["1-2months"]) == 2  # 2 photos de juillet

        assert "3-4months" in resultats
        assert len(resultats["3-4months"]) == 1  # 1 photo de septembre

        assert "5-6months" in resultats
        assert len(resultats["5-6months"]) == 1  # 1 photo de novembre

    def test_calculer_age_mois(self, organiseur):
        """Test le calcul de l'âge en mois."""
        # Test pour les photos de test
        assert organiseur.calculer_age_mois(datetime(2024, 7, 1)) == 1  # 1er juillet
        assert organiseur.calculer_age_mois(datetime(2024, 7, 5)) == 1  # 5 juillet
        assert organiseur.calculer_age_mois(datetime(2024, 9, 1)) == 3  # 1er septembre
        assert organiseur.calculer_age_mois(datetime(2024, 11, 1)) == 5  # 1er novembre

        # Test des cas limites
        assert (
            organiseur.calculer_age_mois(datetime(2024, 6, 1)) == 0
        )  # Jour de naissance
        assert (
            organiseur.calculer_age_mois(datetime(2024, 6, 30)) == 0
        )  # Fin du premier mois

    def test_simuler_organisation(self, organiseur):
        """Test la simulation d'organisation."""
        repartition, erreurs = organiseur.simuler_organisation()

        # Vérifier que la simulation retourne les bons dossiers
        assert "1-2months" in repartition
        assert "3-4months" in repartition
        assert "5-6months" in repartition

        # Vérifier qu'on a bien 4 photos au total
        total_photos = sum(len(photos) for photos in repartition.values())
        assert total_photos == 4

        # Vérifier qu'il n'y a pas d'erreurs
        assert len(erreurs) == 0

    def test_organiser(self, organiseur, temp_test_dir):
        """Test l'organisation réelle des photos."""
        # Organiser les photos
        nombre_deplacees, erreurs = organiseur.organiser()

        # Vérifier que les dossiers ont été créés
        assert (temp_test_dir / "1-2months").exists()
        assert (temp_test_dir / "3-4months").exists()
        assert (temp_test_dir / "5-6months").exists()

        # Vérifier que les photos ont été déplacées
        assert len(list((temp_test_dir / "1-2months").glob("*.jpg"))) == 2
        assert len(list((temp_test_dir / "3-4months").glob("*.jpg"))) == 1
        assert len(list((temp_test_dir / "5-6months").glob("*.jpg"))) == 1

        # Vérifier que le dossier photos est vide
        assert len(list((temp_test_dir / "photos").glob("*.jpg"))) == 0

        # Vérifier les résultats
        assert nombre_deplacees == 4
        assert len(erreurs) == 0

    def test_reinitialiser(self, organiseur, temp_test_dir):
        """Test la réinitialisation après organisation."""
        # D'abord organiser
        organiseur.organiser()

        # Puis réinitialiser
        nombre_remises, erreurs = organiseur.reinitialiser()

        # Vérifier que toutes les photos sont revenues
        assert len(list((temp_test_dir / "photos").glob("*.jpg"))) == 4

        # Vérifier que les dossiers mensuels sont vides
        for dossier in ["1-2months", "3-4months", "5-6months"]:
            if (temp_test_dir / dossier).exists():
                assert len(list((temp_test_dir / dossier).glob("*.jpg"))) == 0

        # Vérifier les résultats
        assert nombre_remises == 4
        assert len(erreurs) == 0

    def test_get_file_type(self, organiseur):
        """Test la détection du type de fichier."""
        assert organiseur.get_file_type(Path("test.jpg")) == "photo"
        assert organiseur.get_file_type(Path("test.jpeg")) == "photo"
        assert organiseur.get_file_type(Path("test.png")) == "photo"
        assert organiseur.get_file_type(Path("test.mp4")) == "video"
        assert organiseur.get_file_type(Path("test.mov")) == "video"
        assert organiseur.get_file_type(Path("test.txt")) == "unknown"

    def test_type_fichiers_videos(self, temp_test_dir):
        """Test avec le type de fichiers vidéos seulement."""
        # Créer une vidéo de test
        video_path = temp_test_dir / "photos" / "20240801_test.mp4"
        video_path.touch()

        organiseur = OrganisateurPhotos(
            dossier_racine=temp_test_dir,
            sous_dossier_photos="photos",
            date_naissance=datetime(2024, 6, 1),
            type_fichiers="🎬 Vidéos uniquement",
        )

        resultats = organiseur.analyser_photos()

        # Vérifier qu'on ne compte que la vidéo
        assert sum(len(photos) for photos in resultats.values()) == 1
        assert "2-3months" in resultats

    def test_type_fichiers_tous(self, temp_test_dir):
        """Test avec tous les types de fichiers."""
        # Créer une vidéo de test
        video_path = temp_test_dir / "photos" / "20240801_test.mp4"
        video_path.touch()

        organiseur = OrganisateurPhotos(
            dossier_racine=temp_test_dir,
            sous_dossier_photos="photos",
            date_naissance=datetime(2024, 6, 1),
            type_fichiers="📸🎬 Photos et Vidéos",
        )

        resultats = organiseur.analyser_photos()

        # Vérifier qu'on compte photos + vidéo
        total = sum(len(photos) for photos in resultats.values())
        assert total == 5  # 4 photos + 1 vidéo

    def test_fichiers_ignores(self, organiseur, temp_test_dir):
        """Test la gestion des fichiers ignorés."""
        # Créer des fichiers qui seront ignorés
        (temp_test_dir / "photos" / "pas_de_date.jpg").touch()
        (temp_test_dir / "photos" / "20240501_avant_naissance.jpg").touch()
        (temp_test_dir / "photos" / "fichier.txt").touch()

        organiseur.analyser_photos()

        # Vérifier les fichiers ignorés (seulement .jpg sont considérés, .txt n'est pas dans extensions_actives)
        assert len(organiseur._fichiers_ignores) == 2

        # Vérifier les raisons
        raisons = dict(organiseur._fichiers_ignores)
        assert "pas_de_date.jpg" in raisons
        assert "format" in raisons["pas_de_date.jpg"].lower()
        assert "20240501_avant_naissance.jpg" in raisons
        assert "naissance" in raisons["20240501_avant_naissance.jpg"].lower()
