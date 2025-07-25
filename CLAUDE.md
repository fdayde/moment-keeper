# CLAUDE.md - Instructions pour Claude

## 🎯 Contexte du Projet

**MomentKeeper** est un organisateur automatique de photos de bébé qui classe les images par mois d'âge basé sur :
- La date de naissance du bébé
- Les dates extraites des noms de fichiers (format `YYYYMMDD_description.jpg`)

## 📁 Architecture du Projet

### Structure des Dossiers
```
moment-keeper/
├── src/moment_keeper/           # Package principal
│   ├── __init__.py             # Version et exports
│   ├── organizer.py            # Logique principale d'organisation
│   ├── photo_copier.py         # Opérations sur fichiers
│   ├── path_manager.py         # Gestion des chemins
│   └── cli.py                  # Interface ligne de commande
├── app.py                      # Interface Streamlit
├── notebooks/                  # Notebooks Jupyter
│   └── classement_photos.ipynb
├── tests/                      # Tests unitaires
├── docs/                       # Documentation
├── requirements.txt            # Dépendances production
├── requirements-dev.txt        # Dépendances développement
├── pyproject.toml             # Configuration du projet
└── .gitignore                 # Exclusions Git
```

### Architecture Logique
- **Dossier racine** : Contient le projet complet
- **Sous-dossier photos** : Contient les photos à organiser (par défaut "photos")
- **Dossiers mensuels** : Créés dans le dossier racine (0-1months, 1-2months, etc.)

## 🔧 Modules Principaux

### `OrganisateurPhotos` (organizer.py)
```python
def __init__(self, dossier_racine: Path, sous_dossier_photos: str, date_naissance: datetime):
```
- **Méthodes clés** :
  - `analyser_photos()` : Analyse et répartit les photos par âge
  - `simuler_organisation()` : Prévisualise sans déplacer les fichiers
  - `organiser()` : Déplace réellement les photos
  - `reinitialiser()` : Remet les photos dans le dossier original
  - `calculer_age_mois()` : Calcul précis basé sur les mois calendaires

### `PhotoCopier` (photo_copier.py)
- Gestion sécurisée des déplacements de fichiers
- Historique des opérations pour rollback
- Gestion des conflits de noms

### `PathManager` (path_manager.py)
- Compatibilité multi-plateforme
- Gestion des chemins absolus/relatifs

## 🖥️ Interfaces Utilisateur

### Interface Streamlit (app.py)
- **Configuration** : Sélection de dossiers avec dialogues natifs (tkinter)
- **Simulation** : Prévisualisation avant organisation
- **Organisation** : Déplacement avec confirmation
- **Debug** : Affichage des fichiers ignorés et raisons

### Interface CLI (cli.py)
```bash
python -m src.moment_keeper.cli /path/to/root 2024-06-25 [options]
```

### Notebook Jupyter
- Version interactive pour exploration et tests
- Import des modules du package principal

## 🛠️ Configuration Technique

### Dépendances
- **Production** : `streamlit>=1.28.0`
- **Développement** : `black`, `isort`, `ruff`, `pytest`

### Outils de Qualité
- **black** : Formatage du code
- **isort** : Tri des imports
- **ruff** : Linting rapide
- **pytest** : Tests unitaires

## 🔄 Workflow Utilisateur

1. **Configuration** :
   - Sélection du dossier racine (ex: `/Users/nom/photos-lucas`)
   - Sélection du sous-dossier photos (ex: `photos`)
   - Date de naissance du bébé

2. **Simulation** :
   - Analyse des photos avec format `YYYYMMDD_*.jpg`
   - Calcul de l'âge en mois à la date de la photo
   - Affichage de la répartition prévue

3. **Organisation** :
   - Création automatique des dossiers mensuels
   - Déplacement des photos vers les dossiers appropriés
   - Gestion des erreurs et conflits

4. **Reset** (optionnel) :
   - Remise de toutes les photos dans le dossier original
   - Suppression des dossiers vides

## 🚨 Points d'Attention

### Calcul de l'Âge
- Utilise un calcul précis basé sur les mois calendaires
- **IMPORTANT** : Ajuste si le jour du mois n'est pas encore atteint
- Exemple : Photo du 21/07/2025, naissance 25/06/2024 → 12 mois (pas 13)

### Gestion des Fichiers
- Format requis : `YYYYMMDD_description.jpg`
- Extensions supportées : `.jpg`, `.jpeg`, `.png`
- Les fichiers sans date ou antérieurs à la naissance sont ignorés

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
pip install -r requirements-dev.txt

# Formatage
black src tests
isort src tests

# Linting
ruff check src tests

# Interface web
streamlit run app.py

# CLI
python -m src.moment_keeper.cli /path/to/project 2024-06-25 --simulate
```

## 📝 Notes pour Claude

- Le projet suit les principes KISS, DRY, YAGNI
- Toujours préférer l'édition de fichiers existants à la création de nouveaux
- Utiliser les modules du package plutôt que des définitions locales
- Les emojis T-Rex (🦖) sont utilisés pour représenter les bébés/enfants
- L'architecture est modulaire pour faciliter les tests et la maintenance