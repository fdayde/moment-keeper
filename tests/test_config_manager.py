"""Tests pour le gestionnaire de configuration."""

import json
from datetime import datetime

import pytest

from moment_keeper.config_manager import ConfigManager


@pytest.fixture
def temp_config_file(tmp_path):
    """Crée un fichier de config temporaire pour les tests."""
    config_file = tmp_path / "test_config.json"
    return config_file


@pytest.fixture
def config_manager(temp_config_file, monkeypatch):
    """Crée un ConfigManager avec un fichier temporaire."""

    # Forcer l'utilisation du fichier temporaire
    def mock_init(self, config_file="momentkeeper_config.json"):
        self.config_file = temp_config_file

    monkeypatch.setattr(ConfigManager, "__init__", mock_init)
    return ConfigManager()


def test_save_config_simple(config_manager):
    """Test sauvegarde d'une config simple."""
    config = {
        "dossier_path": "/test/path",
        "sous_dossier_photos": "photos",
        "language": "fr",
    }

    result = config_manager.save_config(config)
    assert result is True
    assert config_manager.config_file.exists()


def test_save_and_load_config(config_manager):
    """Test sauvegarde puis chargement."""
    config = {
        "dossier_path": "/test/path",
        "sous_dossier_photos": "photos",
        "language": "fr",
        "baby_name": "TestRex",
    }

    # Sauvegarder
    assert config_manager.save_config(config) is True

    # Charger
    loaded_config = config_manager.load_config()
    assert loaded_config is not None
    assert loaded_config["dossier_path"] == "/test/path"
    assert loaded_config["baby_name"] == "TestRex"


def test_save_config_with_date(config_manager):
    """Test sauvegarde avec date de naissance."""
    date_naissance = datetime(2024, 6, 1)
    config = {
        "dossier_path": "/test/path",
        "date_naissance": date_naissance,
    }

    # Sauvegarder
    assert config_manager.save_config(config) is True

    # Vérifier format ISO dans le fichier
    with open(config_manager.config_file, encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data["date_naissance"] == "2024-06-01T00:00:00"


def test_load_config_with_date(config_manager):
    """Test chargement avec conversion de date."""
    config = {
        "dossier_path": "/test/path",
        "date_naissance": datetime(2024, 6, 1),
    }

    # Sauvegarder puis charger
    config_manager.save_config(config)
    loaded_config = config_manager.load_config()

    # Vérifier que la date est convertie en datetime
    assert isinstance(loaded_config["date_naissance"], datetime)
    assert loaded_config["date_naissance"].year == 2024
    assert loaded_config["date_naissance"].month == 6
    assert loaded_config["date_naissance"].day == 1


def test_load_config_nonexistent(config_manager):
    """Test chargement d'un fichier inexistant."""
    result = config_manager.load_config()
    assert result is None


def test_delete_config(config_manager):
    """Test suppression du fichier de config."""
    # Créer un fichier
    config = {"dossier_path": "/test/path"}
    config_manager.save_config(config)
    assert config_manager.config_file.exists()

    # Supprimer
    result = config_manager.delete_config()
    assert result is True
    assert not config_manager.config_file.exists()


def test_delete_config_nonexistent(config_manager):
    """Test suppression d'un fichier inexistant (doit réussir)."""
    result = config_manager.delete_config()
    assert result is True


def test_save_config_invalid_json(config_manager):
    """Test sauvegarde d'une config qui ne peut pas être sérialisée."""
    # Un objet non-sérialisable
    config = {"invalid": object()}

    result = config_manager.save_config(config)
    assert result is False


def test_load_config_corrupted_file(config_manager):
    """Test chargement d'un fichier JSON corrompu."""
    # Créer un fichier JSON invalide
    config_manager.config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_manager.config_file, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")

    result = config_manager.load_config()
    assert result is None
