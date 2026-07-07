"""Tests pour l'extraction de date via EXIF (fallback du nom de fichier)."""

from datetime import datetime
from pathlib import Path

import pytest
from PIL import Image

from moment_keeper.organizer import OrganisateurPhotos, _extract_date_from_exif


def _make_image_with_exif(path: Path, exif_datetime: str | None = None) -> None:
    """Crée une image JPEG avec une date EXIF DateTimeOriginal optionnelle."""
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    if exif_datetime is not None:
        exif = img.getexif()
        exif[36867] = exif_datetime  # DateTimeOriginal
        img.save(path, format="JPEG", exif=exif.tobytes())
    else:
        img.save(path, format="JPEG")


@pytest.fixture
def organiseur_simple(tmp_path):
    photos_dir = tmp_path / "photos"
    photos_dir.mkdir()
    return OrganisateurPhotos(
        dossier_racine=tmp_path,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 1, 1),
        type_fichiers="photos",
    )


def test_extract_date_from_exif_returns_datetime(tmp_path):
    img_path = tmp_path / "photo.jpg"
    _make_image_with_exif(img_path, "2024:06:15 10:30:00")

    result = _extract_date_from_exif(img_path)
    assert result == datetime(2024, 6, 15, 10, 30, 0)


def test_extract_date_from_exif_no_exif(tmp_path):
    img_path = tmp_path / "photo.jpg"
    _make_image_with_exif(img_path, None)

    assert _extract_date_from_exif(img_path) is None


def test_extract_date_from_exif_corrupted_file(tmp_path):
    corrupted = tmp_path / "corrupted.jpg"
    corrupted.write_bytes(b"not an image")

    assert _extract_date_from_exif(corrupted) is None


def test_extract_date_from_exif_missing_file(tmp_path):
    assert _extract_date_from_exif(tmp_path / "ghost.jpg") is None


def test_extraire_date_filename_priority(organiseur_simple, tmp_path):
    """Le nom YYYYMMDD a la priorité sur l'EXIF."""
    # Nom dit 2024-06-15, EXIF dit 2024-12-25
    img_path = tmp_path / "photos" / "20240615_priority.jpg"
    _make_image_with_exif(img_path, "2024:12:25 12:00:00")

    result = organiseur_simple.extraire_date(img_path)
    assert result == datetime(2024, 6, 15)


def test_extraire_date_falls_back_to_exif(organiseur_simple, tmp_path):
    """Sans date dans le nom, on prend l'EXIF."""
    img_path = tmp_path / "photos" / "IMG_001.jpg"
    _make_image_with_exif(img_path, "2024:08:20 09:00:00")

    result = organiseur_simple.extraire_date(img_path)
    assert result == datetime(2024, 8, 20, 9, 0, 0)


def test_extraire_date_no_filename_no_exif_returns_none(organiseur_simple, tmp_path):
    img_path = tmp_path / "photos" / "IMG_002.jpg"
    _make_image_with_exif(img_path, None)

    assert organiseur_simple.extraire_date(img_path) is None


def test_extraire_date_video_uses_only_filename(organiseur_simple, tmp_path):
    """Les vidéos n'ont pas d'EXIF lisible par PIL — fallback skip."""
    video = tmp_path / "photos" / "movie.mp4"
    video.write_bytes(b"\x00" * 100)  # fichier bidon, non lu

    # Pas de YYYYMMDD dans le nom -> retourne None sans crash
    assert organiseur_simple.extraire_date(video) is None

    # Avec date dans le nom -> OK
    dated = tmp_path / "photos" / "20240701_movie.mp4"
    dated.write_bytes(b"\x00" * 100)
    assert organiseur_simple.extraire_date(dated) == datetime(2024, 7, 1)


def test_analyser_photos_picks_up_exif_only_files(organiseur_simple, tmp_path):
    """analyser_photos doit ranger les photos sans nom daté mais avec EXIF."""
    # Une photo dont le nom n'indique rien, mais l'EXIF dit 2024-06-15
    _make_image_with_exif(tmp_path / "photos" / "DSC_0001.jpg", "2024:06:15 10:00:00")
    # Une autre avec nom daté
    _make_image_with_exif(
        tmp_path / "photos" / "20240801_bain.jpg", "2024:08:01 14:00:00"
    )

    repartition = organiseur_simple.analyser_photos()

    # 2024-06-15 → 5 mois (naissance 2024-01-01)
    # 2024-08-01 → 7 mois
    assert "5-6months" in repartition
    assert "7-8months" in repartition
    assert any(p.name == "DSC_0001.jpg" for p in repartition["5-6months"])
