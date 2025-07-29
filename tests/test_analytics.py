"""Tests unitaires pour le module analytics."""
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest
from moment_keeper import analytics


class TestAnalytics:
    """Tests pour le module analytics."""

    def test_extract_photo_data(self, organiseur):
        """Test l'extraction des données des photos."""
        # Analyser d'abord les photos
        organiseur.analyser_photos()

        df = analytics.extract_photo_data(organiseur)

        # Vérifier la structure du DataFrame
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4  # 4 photos de test
        assert set(df.columns) == {
            "file_name",
            "photo_date",
            "age_months",
            "month_folder",
            "file_type",
        }

        # Vérifier les données
        assert df["age_months"].tolist() == [1, 1, 3, 5]
        assert df["month_folder"].tolist() == [
            "1-2months",
            "1-2months",
            "3-4months",
            "5-6months",
        ]
        assert all(df["file_type"] == "photo")

    def test_get_metrics(self, organiseur):
        """Test le calcul des métriques."""
        organiseur.analyser_photos()
        df = analytics.extract_photo_data(organiseur)

        metrics = analytics.calculate_metrics(df)

        # Vérifier les métriques de base
        assert metrics["total_files"] == 4
        assert metrics["total_photos"] == 4
        assert metrics["total_videos"] == 0
        assert metrics["months_with_files"] == 3  # Mois 1, 3 et 5
        assert metrics["files_per_month"] == pytest.approx(4 / 3, 0.1)

        # Vérifier les statistiques par mois
        assert "1" in metrics["files_by_month"]
        assert metrics["files_by_month"]["1"] == 2
        assert metrics["files_by_month"]["3"] == 1
        assert metrics["files_by_month"]["5"] == 1

    def test_generate_insights(self, organiseur):
        """Test la génération d'insights."""
        organiseur.analyser_photos()
        df = analytics.extract_photo_data(organiseur)
        metrics = analytics.calculate_metrics(df)

        insights = analytics.generate_insights(
            metrics, df, organiseur.date_naissance, "Lucas"
        )

        # Vérifier qu'on a des insights
        assert len(insights) > 0
        assert all(isinstance(insight, str) for insight in insights)

        # Vérifier que le prénom est utilisé
        assert any("Lucas" in insight for insight in insights)

    def test_create_distribution_chart(self, organiseur):
        """Test la création du graphique de distribution."""
        organiseur.analyser_photos()
        df = analytics.extract_photo_data(organiseur)

        fig = analytics.create_distribution_chart(df)

        # Vérifier que c'est bien une figure Plotly
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")
        assert len(fig.data) > 0

    def test_create_timeline_chart(self, organiseur):
        """Test la création du graphique timeline."""
        organiseur.analyser_photos()
        df = analytics.extract_photo_data(organiseur)

        fig = analytics.create_timeline_chart(df)

        # Vérifier que c'est bien une figure Plotly
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")
        assert len(fig.data) > 0

    def test_create_monthly_chart(self, organiseur):
        """Test la création du graphique mensuel."""
        organiseur.analyser_photos()
        df = analytics.extract_photo_data(organiseur)

        fig = analytics.create_monthly_chart(df)

        # Vérifier que c'est bien une figure Plotly
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")
        assert len(fig.data) > 0

    def test_get_gallery_photos(self, organiseur, temp_test_dir):
        """Test la récupération des photos pour la galerie."""
        # D'abord organiser les photos
        organiseur.organiser()

        # Test mode aléatoire
        photos = analytics.get_gallery_photos(
            organiseur.dossier_racine, organiseur, mode="random", age_filter=None
        )
        assert len(photos) > 0
        assert all(isinstance(p, dict) for p in photos)
        assert all("file_path" in p and "age_months" in p for p in photos)

        # Test avec filtre d'âge
        photos_filtered = analytics.get_gallery_photos(
            organiseur.dossier_racine, organiseur, mode="random", age_filter=1
        )
        assert len(photos_filtered) == 2  # 2 photos à 1 mois
        assert all(p["age_months"] == 1 for p in photos_filtered)

        # Test mode chronologique
        photos_chrono = analytics.get_gallery_photos(
            organiseur.dossier_racine, organiseur, mode="chronological", age_filter=None
        )
        dates = [p["photo_date"] for p in photos_chrono]
        assert dates == sorted(dates)

        # Test mode highlights (1 photo par mois)
        photos_highlights = analytics.get_gallery_photos(
            organiseur.dossier_racine, organiseur, mode="highlights", age_filter=None
        )
        months = [p["age_months"] for p in photos_highlights]
        assert len(set(months)) == len(months)  # Pas de doublons

    def test_get_age_badge_color(self):
        """Test les couleurs des badges d'âge."""
        # Test différents âges
        assert analytics.get_age_badge_color(0) == "#FFE5E5"  # Rose pâle
        assert analytics.get_age_badge_color(6) == "#E5F0FF"  # Bleu pâle
        assert analytics.get_age_badge_color(12) == "#E5FFE5"  # Vert pâle
        assert analytics.get_age_badge_color(18) == "#FFE5F0"  # Violet pâle
        assert analytics.get_age_badge_color(24) == "#FFFAE5"  # Jaune pâle
        assert analytics.get_age_badge_color(30) == "#F0E5FF"  # Lavande

    def test_format_age(self):
        """Test le formatage de l'âge."""
        # Test différents âges
        assert analytics.format_age(0) == "Nouveau-né"
        assert analytics.format_age(1) == "1 mois"
        assert analytics.format_age(6) == "6 mois"
        assert analytics.format_age(12) == "1 an"
        assert analytics.format_age(18) == "1 an et demi"
        assert analytics.format_age(24) == "2 ans"
        assert analytics.format_age(30) == "2 ans et demi"

    def test_empty_data(self):
        """Test avec un organiseur sans photos."""
        organiseur = MagicMock()
        organiseur.photos_par_dossier = {}
        organiseur.date_naissance = datetime(2024, 6, 1)
        organiseur.dossier_racine = Path("/fake/path")
        organiseur.extensions_actives = [".jpg", ".jpeg", ".png"]

        # Mock pour éviter d'itérer sur un vrai dossier
        organiseur.dossier_racine.iterdir = MagicMock(return_value=[])

        # Test extraction vide
        df = analytics.extract_photo_data(organiseur)
        assert len(df) == 0

        # Test métriques vides
        metrics = analytics.calculate_metrics(df)
        assert metrics["total_photos"] == 0
        assert metrics["avg_photos_per_month"] == 0

        # Test insights vides
        insights = analytics.generate_insights(
            metrics, df, organiseur.date_naissance, ""
        )
        assert len(insights) > 0  # Doit toujours y avoir au moins un insight
