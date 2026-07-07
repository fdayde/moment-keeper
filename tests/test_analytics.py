"""Tests pour le module analytics."""

from datetime import datetime

import pandas as pd
import pytest

from moment_keeper.analytics import (
    _cache_signature,
    age_to_month_name,
    calculate_metrics,
    extract_photo_data,
    find_gaps,
    generate_insights,
    get_chronological_photos,
    get_gallery_data,
    get_highlight_photos,
    get_photo_caption_with_age,
    get_photos_by_mode,
    get_random_photos_for_month,
    get_timeline_photos,
    photos_grouped_by_age,
)
from moment_keeper.config import (
    ALL_MONTHS_SENTINEL,
    FILE_TYPES,
    UNSORTED_SENTINEL,
)
from moment_keeper.translations import Translator

# ---------- extract_photo_data / get_gallery_data ----------


def test_extract_photo_data(organiseur):
    df = extract_photo_data(organiseur)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    assert {"fichier", "date", "age_mois", "type", "jour_semaine"} <= set(df.columns)


def test_get_gallery_data_unsorted(organiseur):
    """Avant organisation, les photos sont sous la sentinelle UNSORTED."""
    gallery_data = get_gallery_data(organiseur)

    assert isinstance(gallery_data, dict)
    assert UNSORTED_SENTINEL in gallery_data
    assert len(gallery_data[UNSORTED_SENTINEL]) == 4


def test_get_gallery_data_after_organize(organiseur):
    """Après organisation, les photos sont sous les dossiers mensuels."""
    organiseur.organiser()
    gallery_data = get_gallery_data(organiseur)

    assert UNSORTED_SENTINEL not in gallery_data
    assert "1-2months" in gallery_data
    assert "3-4months" in gallery_data
    assert "5-6months" in gallery_data


# ---------- calculate_metrics ----------


def test_calculate_metrics_empty():
    df = pd.DataFrame()
    metrics = calculate_metrics(df)

    assert metrics["total_photos"] == 0
    assert metrics["total_videos"] == 0
    assert metrics["periode_couverte"] == 0
    assert metrics["derniere_photo"] is None
    assert metrics["max_gap"] == 0


def test_calculate_metrics_photos_only(organiseur):
    df = extract_photo_data(organiseur)
    metrics = calculate_metrics(df, type_fichiers=FILE_TYPES["photos_only"])

    assert metrics["total_photos"] == 4
    assert metrics["total_videos"] == 0


def test_calculate_metrics_both_mode(organiseur, temp_test_dir):
    (temp_test_dir / "photos" / "20240801_test.mp4").touch()
    from moment_keeper.organizer import OrganisateurPhotos

    org = OrganisateurPhotos(
        dossier_racine=temp_test_dir,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 6, 1),
        type_fichiers=FILE_TYPES["both"],
    )
    df = extract_photo_data(org)
    metrics = calculate_metrics(df, type_fichiers=FILE_TYPES["both"])

    assert metrics["total_photos"] == 4
    assert metrics["total_videos"] == 1
    assert metrics["total_fichiers"] == 5


def test_get_gallery_data_includes_videos_in_both_mode(temp_test_dir):
    """En mode 'both', les vidéos apparaissent dans gallery_data."""
    from moment_keeper.organizer import OrganisateurPhotos

    (temp_test_dir / "photos" / "20240801_test.mp4").touch()
    org = OrganisateurPhotos(
        dossier_racine=temp_test_dir,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 6, 1),
        type_fichiers=FILE_TYPES["both"],
    )

    gallery = get_gallery_data(org)
    all_files = [f for files in gallery.values() for f in files]
    names = {f.name for f in all_files}
    assert "20240801_test.mp4" in names
    assert sum(1 for n in names if n.endswith(".jpg")) == 4


def test_get_gallery_data_videos_only_mode(temp_test_dir):
    """En mode videos_only, gallery_data ne contient que les vidéos."""
    from moment_keeper.organizer import OrganisateurPhotos

    (temp_test_dir / "photos" / "20240801_test.mp4").touch()
    org = OrganisateurPhotos(
        dossier_racine=temp_test_dir,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 6, 1),
        type_fichiers=FILE_TYPES["videos_only"],
    )

    gallery = get_gallery_data(org)
    all_files = [f for files in gallery.values() for f in files]
    assert all(f.suffix.lower() == ".mp4" for f in all_files)
    assert len(all_files) == 1


# ---------- find_gaps ----------


def test_find_gaps_empty():
    assert find_gaps(pd.DataFrame()) == []


def test_find_gaps_returns_gaps_above_threshold(organiseur):
    df = extract_photo_data(organiseur)
    # Default threshold = 5 days. Test photos: 2024-07-01, 07-05, 09-01, 11-01
    gaps = find_gaps(df, min_gap_days=5)
    assert len(gaps) >= 2  # 07-05→09-01 et 09-01→11-01
    for start, end, days in gaps:
        assert days >= 5
        assert end > start


def test_find_gaps_high_threshold_excludes_short(organiseur):
    df = extract_photo_data(organiseur)
    long_gaps = find_gaps(df, min_gap_days=70)
    assert all(g[2] >= 70 for g in long_gaps)


# ---------- age_to_month_name ----------


def test_age_to_month_name_fr():
    naissance = datetime(2024, 6, 1)
    assert age_to_month_name(0, naissance, "fr") == "Juin"
    assert age_to_month_name(2, naissance, "fr") in ("Août", "Juillet")


def test_age_to_month_name_en():
    naissance = datetime(2024, 6, 1)
    name = age_to_month_name(0, naissance, "en")
    assert name in ("June", "July")


# ---------- Gallery modes ----------


@pytest.fixture
def gallery_data_organized(organiseur):
    organiseur.organiser()
    return get_gallery_data(organiseur)


def test_get_random_photos_specific_month(gallery_data_organized):
    photos = get_random_photos_for_month(gallery_data_organized, "1-2months", 2)
    assert len(photos) == 2
    assert all(p.suffix.lower() == ".jpg" for p in photos)


def test_get_random_photos_all(gallery_data_organized):
    photos = get_random_photos_for_month(
        gallery_data_organized, ALL_MONTHS_SENTINEL, 10
    )
    assert len(photos) == 4  # toutes les photos


def test_get_random_photos_unknown_month(gallery_data_organized):
    assert get_random_photos_for_month(gallery_data_organized, "99-100months", 3) == []


def test_get_chronological_photos_specific_month(gallery_data_organized, organiseur):
    photos = get_chronological_photos(
        gallery_data_organized, organiseur, "1-2months", 10
    )
    assert len(photos) == 2
    # ordre décroissant : la plus récente d'abord
    d1 = organiseur.extraire_date_nom_fichier(photos[0].name)
    d2 = organiseur.extraire_date_nom_fichier(photos[1].name)
    assert d1 >= d2


def test_get_chronological_photos_all(gallery_data_organized, organiseur):
    photos = get_chronological_photos(
        gallery_data_organized, organiseur, ALL_MONTHS_SENTINEL, 10
    )
    dates = [organiseur.extraire_date_nom_fichier(p.name) for p in photos]
    assert dates == sorted(dates, reverse=True)


def test_get_highlight_photos(gallery_data_organized, organiseur):
    photos = get_highlight_photos(
        gallery_data_organized, organiseur, ALL_MONTHS_SENTINEL, 5
    )
    assert 0 < len(photos) <= 5


def test_get_timeline_photos_from_organized(gallery_data_organized, organiseur):
    photos = get_timeline_photos(gallery_data_organized, organiseur, 6)
    assert 0 < len(photos) <= 3  # 3 mois différents dans les données de test


def test_get_timeline_photos_from_unsorted(organiseur):
    """Si rien n'est organisé, timeline construit à partir de UNSORTED."""
    gallery_data = get_gallery_data(organiseur)
    photos = get_timeline_photos(gallery_data, organiseur, 6)
    assert len(photos) > 0


def test_get_photos_by_mode_dispatches(gallery_data_organized, organiseur):
    # Random
    r = get_photos_by_mode(
        gallery_data_organized, organiseur, "random", ALL_MONTHS_SENTINEL, 3
    )
    assert len(r) == 3
    # Chronological
    c = get_photos_by_mode(
        gallery_data_organized,
        organiseur,
        "chronological",
        ALL_MONTHS_SENTINEL,
        2,
    )
    assert len(c) == 2
    # Highlights
    h = get_photos_by_mode(
        gallery_data_organized,
        organiseur,
        "highlights",
        ALL_MONTHS_SENTINEL,
        2,
    )
    assert len(h) > 0
    # Timeline (ignore selected_month)
    t = get_photos_by_mode(
        gallery_data_organized,
        organiseur,
        "timeline",
        ALL_MONTHS_SENTINEL,
        6,
    )
    assert len(t) > 0


def test_get_photos_by_mode_unknown_falls_back_to_random(
    gallery_data_organized, organiseur
):
    r = get_photos_by_mode(
        gallery_data_organized, organiseur, "mode-inconnu", ALL_MONTHS_SENTINEL, 2
    )
    assert len(r) == 2


# ---------- Time-lapse (photos_grouped_by_age) ----------


def test_photos_grouped_by_age_groups_correctly(organiseur):
    """Les photos test 2024 (naissance 06-01) couvrent 3 ages : 1, 3, 5 mois."""
    gallery = get_gallery_data(organiseur)
    groups = photos_grouped_by_age(gallery, organiseur)

    # 2 photos de juillet → age 1 mois
    assert 1 in groups
    assert len(groups[1]) == 2
    # 1 photo de septembre → age 3 mois
    assert 3 in groups
    assert len(groups[3]) == 1
    # 1 photo de novembre → age 5 mois
    assert 5 in groups
    assert len(groups[5]) == 1


def test_photos_grouped_by_age_empty_when_no_photos(tmp_path):
    """Galerie vide → dict vide."""
    from moment_keeper.organizer import OrganisateurPhotos

    (tmp_path / "photos").mkdir()
    org = OrganisateurPhotos(
        dossier_racine=tmp_path,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 1, 1),
        type_fichiers=FILE_TYPES["photos_only"],
    )
    gallery = get_gallery_data(org)
    assert photos_grouped_by_age(gallery, org) == {}


# ---------- Caption + insights + signature ----------


def test_get_photo_caption_with_age_returns_html(organiseur):
    df = extract_photo_data(organiseur)
    photo_path = df.iloc[0]["fichier"]
    # Le fichier dans le dossier source — reconstruire path
    full_path = organiseur.dossier_source / photo_path
    tr = Translator("fr")
    caption = get_photo_caption_with_age(full_path, organiseur, tr)
    assert "age-badge" in caption
    assert "🦖" in caption


def test_generate_insights_empty():
    tr = Translator("fr")
    result = generate_insights(
        pd.DataFrame(), {}, datetime(2024, 6, 1), FILE_TYPES["photos_only"], tr
    )
    assert len(result) == 1  # message "analyze_first"


def test_generate_insights_nonempty(organiseur):
    df = extract_photo_data(organiseur)
    metrics = calculate_metrics(df, type_fichiers=FILE_TYPES["photos_only"])
    tr = Translator("fr")
    insights = generate_insights(
        df, metrics, organiseur.date_naissance, FILE_TYPES["photos_only"], tr
    )
    assert len(insights) > 0
    assert all(isinstance(s, str) for s in insights)


def test_cache_signature_changes_with_date(organiseur, temp_test_dir):
    """La signature change si date_naissance change."""
    from moment_keeper.organizer import OrganisateurPhotos

    sig_a = _cache_signature(organiseur)
    other = OrganisateurPhotos(
        dossier_racine=temp_test_dir,
        sous_dossier_photos="photos",
        date_naissance=datetime(2023, 1, 1),
        type_fichiers=FILE_TYPES["photos_only"],
    )
    sig_b = _cache_signature(other)
    assert sig_a != sig_b


def test_cache_signature_stable_for_same_organiseur(organiseur):
    """Appels identiques → même signature (cache hit attendu)."""
    assert _cache_signature(organiseur) == _cache_signature(organiseur)
