"""Tests pour le module analytics."""

import pandas as pd

from moment_keeper.analytics import extract_photo_data, get_gallery_data


def test_extract_photo_data(organiseur):
    """Test extraction des données depuis l'organisateur."""
    df = extract_photo_data(organiseur)

    # Vérifier que c'est un DataFrame avec des données
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    # Vérifier les colonnes essentielles
    assert "fichier" in df.columns
    assert "date" in df.columns
    assert "age_mois" in df.columns


def test_get_gallery_data(organiseur):
    """Test récupération des données pour la galerie."""
    gallery_data = get_gallery_data(organiseur)

    # Vérifier que c'est un dict avec des données
    assert isinstance(gallery_data, dict)
    assert len(gallery_data) > 0
