# CLAUDE.md - Instructions pour Claude

## 🎯 Contexte du Projet

**MomentKeeper** est un organisateur automatique de photos et vidéos de bébé qui classe les fichiers média par mois d'âge basé sur :
- La date de naissance du bébé
- Les dates extraites des noms de fichiers (format `YYYYMMDD_description.jpg`)

### Fonctionnalités récentes ajoutées :
- **Galerie interactive** avec 4 modes de visualisation
- **Badges d'âge** sur les photos montrant l'âge du bébé
- **Prénom du bébé** pour personnaliser l'expérience
- **Persistance de configuration** automatique
- **Navigation améliorée** avec tous les onglets toujours accessibles

## 📁 Architecture du Projet

### Structure des Dossiers
```
moment-keeper/
├── src/moment_keeper/           # Package principal
│   ├── __init__.py             # Version et exports
│   ├── organizer.py            # Logique principale d'organisation
│   ├── photo_copier.py         # Opérations sur fichiers
│   ├── analytics.py            # Analyse et statistiques
│   ├── config.py               # Configuration centralisée
│   ├── config_manager.py       # Persistance de la configuration
│   ├── theme.py                # Thème et styles UI
│   ├── translations.py         # Support multilingue
│   ├── logger.py               # Logging centralisé
│   ├── utils.py                # Utilitaires partagés
│   └── cli.py                  # Lanceur CLI Streamlit
├── app.py                      # Interface Streamlit
├── notebooks/                  # Notebooks Jupyter
│   └── classement_photos.ipynb
├── tests/                      # Tests unitaires
├── docs/                       # Documentation
├── pyproject.toml              # Configuration du projet et dépendances (uv)
└── .gitignore                  # Exclusions Git
```

### Architecture Logique
- **Dossier racine** : Contient le projet complet
- **Sous-dossier photos** : Contient les photos à organiser (par défaut "photos")
- **Dossiers mensuels** : Créés dans le dossier racine (0-1months, 1-2months, etc.)

## 🔧 Modules Principaux

### `OrganisateurPhotos` (organizer.py)
```python
def __init__(self, dossier_racine: Path, sous_dossier_photos: str, date_naissance: datetime, type_fichiers: str):
```
- **Méthodes clés** :
  - `analyser_photos()` : Analyse et répartit les photos par âge
  - `simuler_organisation()` : Prévisualise sans déplacer les fichiers
  - `organiser()` : Déplace réellement les photos
  - `reinitialiser()` : Remet les photos dans le dossier original
  - `calculer_age_mois()` : Calcul précis basé sur les mois calendaires
  - `get_file_type()` : Détermine si c'est une photo ou vidéo

### `PhotoCopier` (photo_copier.py)
- Gestion sécurisée des déplacements de fichiers
- Gestion des conflits de noms
- Méthodes simples et robustes

### `Analytics` (analytics.py)
- Extraction et analyse des données
- Calcul des métriques (total, moyenne, gaps)
- Génération d'insights contextuels
- Création de graphiques interactifs
- Gestion de la galerie photos avec 4 modes d'affichage
- Calcul et affichage de l'âge du bébé sur les photos

### `Config` (config.py)
- Constantes centralisées
- Extensions de fichiers supportées
- Seuils pour les insights
- Configuration des graphiques

### `ConfigManager` (config_manager.py)
- Sauvegarde automatique de la configuration
- Stockage dans l'emplacement système approprié : Windows `%APPDATA%/momentkeeper/`, macOS `~/Library/Application Support/momentkeeper/`, Linux `~/.config/momentkeeper/`
- En développement, une config locale dans `data/user-config/` est prioritaire (sauf en exécutable packagé)
- Chargement au démarrage de l'application
- Gestion des conversions de dates pour JSON

### `Theme` (theme.py)
- Palette de couleurs T-Rex pastel
- Styles CSS personnalisés
- Thème cohérent pour l'UI
- Styles pour les badges d'âge dans la galerie

### `Translations` (translations.py)
- Support multilingue (FR/EN)
- Tous les textes de l'interface
- Traductions contextuelles
- Préférence de langue persistante

## 🖥️ Interfaces Utilisateur

### Interface Streamlit (app.py)
- **Configuration** :
  - Sélection de dossiers avec dialogues natifs (tkinter)
  - Champ pour le prénom du bébé (personnalisation)
  - Sélection du type de fichiers (photos/vidéos/les deux)
  - Sauvegarde automatique de tous les paramètres
- **Navigation** : Tous les onglets toujours accessibles
- **Simulation** : Prévisualisation avant organisation
- **Organisation** : Déplacement avec confirmation
- **Analytics** : Tableaux de bord avec métriques et graphiques
- **Insights** : Découverte de patterns dans les habitudes photo
- **Galerie** :
  - 4 modes d'affichage (aléatoire, chronologique, highlights, timeline)
  - Badges d'âge sur chaque photo
  - Slider adaptatif basé sur l'âge actuel du bébé
- **Debug** : Affichage des fichiers ignorés et raisons


### Notebook Jupyter
- Version interactive pour exploration et tests
- Import des modules du package principal

## 🛠️ Configuration Technique

### Dépendances
- **Production** : `streamlit`, `pandas`, `plotly`, `Pillow`, `pillow-heif`
- **Développement** : `pytest`, `pytest-cov`, `ruff`, `pre-commit`

### Outils de Qualité
- **ruff** : Linting et formatage (la règle `I` couvre le tri des imports)
- **pytest** : Tests unitaires
- **pre-commit** : Hooks automatiques avant commit

## 🔄 Workflow Utilisateur

1. **Configuration** :
   - Sélection du dossier racine (ex: `/Users/nom/photos-lucas`)
   - Sélection du sous-dossier photos (ex: `photos`)
   - Date de naissance du bébé
   - Prénom du bébé (optionnel)
   - Type de fichiers à organiser
   - **Toute la configuration est sauvegardée automatiquement**

2. **Simulation** :
   - Analyse des photos avec format `YYYYMMDD_*.jpg`
   - Calcul de l'âge en mois à la date de la photo
   - Affichage de la répartition prévue

3. **Organisation** :
   - Création automatique des dossiers mensuels
   - Déplacement des photos vers les dossiers appropriés
   - Gestion des erreurs et conflits

4. **Exploration** :
   - Analytics : métriques et graphiques
   - Insights : découverte de patterns
   - Galerie : visualisation des photos organisées

5. **Reset** (optionnel) :
   - Remise de toutes les photos dans le dossier original
   - Suppression des dossiers vides

## 🚨 Points d'Attention

### Calcul de l'Âge
- Utilise un calcul précis basé sur les mois calendaires
- **IMPORTANT** : Ajuste si le jour du mois n'est pas encore atteint
- Exemple : Photo du 21/07/2025, naissance 25/06/2024 → 12 mois (pas 13)

### Gestion des Fichiers
- Format requis : `YYYYMMDD_description.ext`
- Extensions photos : `.jpg`, `.jpeg`, `.png`, `.heic`, `.webp`
- Extensions vidéos : `.mp4`, `.mov`, `.avi`, `.mkv`, `.m4v`, `.3gp`, `.wmv`
- Les fichiers sans date ou antérieurs à la naissance sont ignorés
- Sélection possible : photos seules, vidéos seules, ou les deux

### Sécurité
- Simulation obligatoire avant organisation
- Vérification d'existence des fichiers
- Gestion des conflits de noms
- Possibilité de rollback complet

## 🐛 Debugging Common

### Erreurs Fréquentes
1. **"Aucune photo trouvée"** : Vérifier le format des noms de fichiers
2. **"Dossier n'existe pas"** : Vérifier les chemins de configuration
3. **Import du notebook** : Utiliser `os.getcwd()` au lieu de `__file__`

### Logs et Debug
- Les fichiers ignorés sont stockés dans `organiseur._fichiers_ignores`
- Affichage des raisons d'exclusion dans l'interface Streamlit
- Messages d'erreur détaillés pour chaque opération

## 🚀 Commandes de Développement

```bash
# Installation
uv sync --extra dev

# Configuration pre-commit (recommandé)
uv run pre-commit install

# Linting manuel
uv run ruff check src tests app.py

# Formatage manuel
uv run ruff format src tests app.py

# Tests
uv run pytest

# Vérification pre-commit
uv run pre-commit run --all-files

# Interface web
uv run streamlit run app.py
```

## 📝 Notes pour Claude

- Le projet suit les principes KISS, DRY, YAGNI
- Toujours préférer l'édition de fichiers existants à la création de nouveaux
- Utiliser les modules du package plutôt que des définitions locales
- Les emojis T-Rex (🦖) sont utilisés pour représenter les bébés/enfants
- L'architecture est modulaire pour faciliter les tests et la maintenance
- Le refactoring récent a séparé la logique métier de l'UI
- path_manager.py a été supprimé (utilisation directe de pathlib)
- Toute la configuration est dans config.py
- Les styles sont dans theme.py
- L'analyse et les statistiques sont dans analytics.py
- La configuration est persistante grâce à ConfigManager
- La galerie offre 4 modes de visualisation différents
- Les badges d'âge sont calculés et affichés sur les photos
- Tous les onglets sont toujours accessibles pour une meilleure navigation
