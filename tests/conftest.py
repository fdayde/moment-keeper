"""Configuration des fixtures pour les tests pytest."""
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from moment_keeper.organizer import OrganisateurPhotos


@pytest.fixture
def test_data_dir():
    """Retourne le chemin vers les données de test."""
    return Path(__file__).parent.parent / "data" / "test"


@pytest.fixture
def temp_test_dir(test_data_dir):
    """Crée un dossier temporaire avec une copie des photos de test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)

        # Copier la structure de test
        photos_src = test_data_dir / "photos"
        photos_dst = temp_path / "photos"

        # Créer le dossier photos et copier les fichiers
        photos_dst.mkdir()
        for photo in photos_src.glob("*.jpg"):
            shutil.copy2(photo, photos_dst)

        yield temp_path


@pytest.fixture
def organiseur(temp_test_dir):
    """Crée une instance d'OrganisateurPhotos avec les données de test."""
    return OrganisateurPhotos(
        dossier_racine=temp_test_dir,
        sous_dossier_photos="photos",
        date_naissance=datetime(2024, 6, 1),  # Date de naissance pour les tests
        type_fichiers="photos",
    )


@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock les fonctions Streamlit pour les tests."""
    import sys
    from unittest.mock import MagicMock

    # Créer un mock pour streamlit
    mock_st = MagicMock()

    # Ajouter les méthodes couramment utilisées
    mock_st.session_state = {}
    mock_st.set_page_config = MagicMock()
    mock_st.title = MagicMock()
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.write = MagicMock()
    mock_st.error = MagicMock()
    mock_st.success = MagicMock()
    mock_st.info = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.checkbox = MagicMock(return_value=False)
    mock_st.selectbox = MagicMock(return_value=None)
    mock_st.date_input = MagicMock(return_value=datetime.now().date())
    mock_st.text_input = MagicMock(return_value="")
    mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
    mock_st.container = MagicMock()
    mock_st.expander = MagicMock()
    mock_st.sidebar = MagicMock()
    mock_st.tabs = MagicMock(return_value=[MagicMock()])
    mock_st.metric = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.image = MagicMock()
    mock_st.plotly_chart = MagicMock()
    mock_st.dataframe = MagicMock()
    mock_st.json = MagicMock()
    mock_st.code = MagicMock()
    mock_st.spinner = MagicMock()
    mock_st.progress = MagicMock()
    mock_st.empty = MagicMock()
    mock_st.form = MagicMock()
    mock_st.form_submit_button = MagicMock(return_value=False)
    mock_st.file_uploader = MagicMock(return_value=None)
    mock_st.download_button = MagicMock(return_value=False)

    # Injecter le mock
    monkeypatch.setitem(sys.modules, "streamlit", mock_st)

    return mock_st
