"""Tests unitaires pour le module photo_copier."""
import tempfile
from pathlib import Path

import pytest
from moment_keeper.photo_copier import PhotoCopier


class TestPhotoCopier:
    """Tests pour la classe PhotoCopier."""

    @pytest.fixture
    def temp_dirs(self):
        """Crée des dossiers temporaires pour les tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir)
            source_dir = temp_path / "source"
            dest_dir = temp_path / "dest"

            source_dir.mkdir()
            dest_dir.mkdir()

            yield source_dir, dest_dir

    def test_copier_fichier_simple(self, temp_dirs):
        """Test la copie d'un fichier simple."""
        source_dir, dest_dir = temp_dirs

        # Créer un fichier source
        source_file = source_dir / "test.jpg"
        source_file.write_text("contenu test")

        # Déplacer le fichier
        copier = PhotoCopier()
        dest_file = copier.deplacer_fichier(source_file, dest_dir)

        # Vérifications
        assert dest_file.exists()
        assert dest_file.name == "test.jpg"
        assert dest_file.read_text() == "contenu test"
        assert not source_file.exists()  # Le fichier source doit être déplacé

    def test_copier_fichier_conflit_nom(self, temp_dirs):
        """Test la copie avec gestion des conflits de noms."""
        source_dir, dest_dir = temp_dirs

        # Créer un fichier qui existe déjà dans la destination
        existing_file = dest_dir / "test.jpg"
        existing_file.write_text("fichier existant")

        # Créer le fichier source
        source_file = source_dir / "test.jpg"
        source_file.write_text("nouveau fichier")

        # Déplacer le fichier
        copier = PhotoCopier()
        # PhotoCopier.deplacer_fichier lance une exception si le fichier existe déjà
        with pytest.raises(FileExistsError):
            copier.deplacer_fichier(source_file, dest_dir)

        # Vérifications
        assert existing_file.exists()
        assert existing_file.read_text() == "fichier existant"  # Original non modifié
        assert source_file.exists()  # Source non déplacée car erreur

    def test_copier_fichier_avec_copie(self, temp_dirs):
        """Test la copie réelle d'un fichier."""
        source_dir, dest_dir = temp_dirs

        # Créer le fichier source
        source_file = source_dir / "test.jpg"
        source_file.write_text("contenu test")

        # Copier le fichier
        copier = PhotoCopier()
        dest_file = copier.copier_fichier(source_file, dest_dir)

        # Vérifications
        assert dest_file.exists()
        assert dest_file.name == "test.jpg"
        assert dest_file.read_text() == "contenu test"
        assert (
            source_file.exists()
        )  # Le fichier source doit toujours exister (copie, pas déplacement)

    def test_deplacer_fichier_preserve_extension(self, temp_dirs):
        """Test que l'extension est préservée lors des conflits."""
        source_dir, dest_dir = temp_dirs

        # Créer un fichier existant avec extension complexe
        (dest_dir / "photo.jpeg").touch()

        # Créer le fichier source
        source_file = source_dir / "photo.jpeg"
        source_file.touch()

        # Déplacer le fichier
        copier = PhotoCopier()

        # Vérifier que l'exception est levée pour le conflit
        with pytest.raises(FileExistsError):
            copier.deplacer_fichier(source_file, dest_dir)

    def test_copier_fichier_erreur_source_inexistant(self, temp_dirs):
        """Test l'erreur quand le fichier source n'existe pas."""
        source_dir, dest_dir = temp_dirs

        source_file = source_dir / "inexistant.jpg"

        copier = PhotoCopier()
        with pytest.raises(FileNotFoundError):
            copier.deplacer_fichier(source_file, dest_dir)

    def test_copier_fichier_erreur_dest_inexistant(self, temp_dirs):
        """Test l'erreur quand le dossier destination n'existe pas."""
        source_dir, _ = temp_dirs

        source_file = source_dir / "test.jpg"
        source_file.touch()

        dest_dir = source_dir / "dossier_inexistant"

        copier = PhotoCopier()
        # PhotoCopier crée le dossier s'il n'existe pas
        dest_file = copier.deplacer_fichier(source_file, dest_dir)
        assert dest_file.exists()
        assert dest_dir.exists()

    def test_deplacer_fichier_meme_source_dest(self, temp_dirs):
        """Test le déplacement quand source et destination sont identiques."""
        source_dir, _ = temp_dirs

        source_file = source_dir / "test.jpg"
        source_file.write_text("contenu")

        # Déplacer dans le même dossier
        copier = PhotoCopier()

        # Cela devrait lever une exception car le fichier existe déjà
        with pytest.raises(FileExistsError):
            copier.deplacer_fichier(source_file, source_dir)

    def test_copier_fichier_avec_metadonnees(self, temp_dirs):
        """Test que les métadonnées sont préservées lors de la copie."""
        source_dir, dest_dir = temp_dirs

        # Créer un fichier source
        source_file = source_dir / "test.jpg"
        source_file.write_text("contenu test")

        # Récupérer les stats avant copie
        stats_before = source_file.stat()

        # Déplacer le fichier
        copier = PhotoCopier()
        dest_file = copier.deplacer_fichier(source_file, dest_dir)

        # Vérifier que les dates sont préservées
        stats_after = dest_file.stat()
        assert (
            abs(stats_after.st_mtime - stats_before.st_mtime) < 1
        )  # Tolérance d'1 seconde
