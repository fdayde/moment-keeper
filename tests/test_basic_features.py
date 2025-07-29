"""Tests unitaires basiques pour valider les fonctionnalités principales."""

import pytest


def test_organisation_complete(organiseur, temp_test_dir):
    """Test complet du processus d'organisation des photos."""
    # 1. Analyser les photos
    repartition = organiseur.analyser_photos()

    # Vérifier la répartition attendue
    assert len(repartition) == 3  # 3 dossiers différents
    assert "1-2months" in repartition
    assert "3-4months" in repartition
    assert "5-6months" in repartition
    assert len(repartition["1-2months"]) == 2
    assert len(repartition["3-4months"]) == 1
    assert len(repartition["5-6months"]) == 1

    # 2. Simuler l'organisation
    simulation, erreurs = organiseur.simuler_organisation()
    assert len(erreurs) == 0
    assert simulation == repartition

    # 3. Organiser réellement
    nombre_deplacees, erreurs = organiseur.organiser()
    assert nombre_deplacees == 4
    assert len(erreurs) == 0

    # Vérifier la création des dossiers
    assert (temp_test_dir / "1-2months").exists()
    assert (temp_test_dir / "3-4months").exists()
    assert (temp_test_dir / "5-6months").exists()

    # Vérifier le déplacement des photos
    assert len(list((temp_test_dir / "1-2months").glob("*.jpg"))) == 2
    assert len(list((temp_test_dir / "3-4months").glob("*.jpg"))) == 1
    assert len(list((temp_test_dir / "5-6months").glob("*.jpg"))) == 1
    assert len(list((temp_test_dir / "photos").glob("*.jpg"))) == 0

    # 4. Réinitialiser
    nombre_remises, erreurs = organiseur.reinitialiser()
    assert nombre_remises == 4
    assert len(erreurs) == 0

    # Vérifier que les photos sont revenues
    assert len(list((temp_test_dir / "photos").glob("*.jpg"))) == 4


def test_extraction_donnees_analytics(organiseur):
    """Test l'extraction des données pour l'analytics."""
    from moment_keeper import analytics

    # Analyser les photos
    organiseur.analyser_photos()

    # Extraire les données
    df = analytics.extract_photo_data(organiseur)

    # Vérifications basiques
    assert len(df) == 4
    assert "age_mois" in df.columns
    assert "date" in df.columns
    assert "type" in df.columns

    # Vérifier les âges
    ages = df["age_mois"].tolist()
    assert sorted(ages) == [1, 1, 3, 5]

    # Vérifier les types
    assert all(df["type"] == "photo")


def test_calcul_metriques(organiseur):
    """Test le calcul des métriques."""
    from moment_keeper import analytics

    # Analyser et extraire
    organiseur.analyser_photos()
    df = analytics.extract_photo_data(organiseur)

    # Calculer les métriques
    metrics = analytics.calculate_metrics(df, type_fichiers="📸 Photos uniquement")

    # Vérifications
    assert metrics["total_photos"] == 4
    assert metrics["total_videos"] == 0
    assert metrics["total_fichiers"] == 4
    assert metrics["periode_couverte"] == 6  # De 0 à 5 mois
    assert metrics["moyenne_par_mois"] == pytest.approx(4 / 6, 0.1)


def test_copie_fichier(temp_test_dir):
    """Test la copie de fichier avec PhotoCopier."""
    from moment_keeper.photo_copier import PhotoCopier

    # Créer les dossiers
    source_dir = temp_test_dir / "source"
    dest_dir = temp_test_dir / "destination"
    source_dir.mkdir()
    dest_dir.mkdir()

    # Créer un fichier
    source_file = source_dir / "test.jpg"
    source_file.write_text("contenu test")

    # Copier le fichier
    copier = PhotoCopier()
    dest_file = copier.copier_fichier(source_file, dest_dir)

    # Vérifications
    assert dest_file.exists()
    assert dest_file.read_text() == "contenu test"
    assert source_file.exists()  # La source reste


def test_deplacement_fichier(temp_test_dir):
    """Test le déplacement de fichier avec PhotoCopier."""
    from moment_keeper.photo_copier import PhotoCopier

    # Créer les dossiers
    source_dir = temp_test_dir / "source"
    dest_dir = temp_test_dir / "destination"
    source_dir.mkdir()
    dest_dir.mkdir()

    # Créer un fichier
    source_file = source_dir / "test.jpg"
    source_file.write_text("contenu test")

    # Déplacer le fichier
    copier = PhotoCopier()
    dest_file = copier.deplacer_fichier(source_file, dest_dir)

    # Vérifications
    assert dest_file.exists()
    assert dest_file.read_text() == "contenu test"
    assert not source_file.exists()  # La source est supprimée
