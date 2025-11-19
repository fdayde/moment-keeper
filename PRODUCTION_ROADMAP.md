# 🚀 MomentKeeper - Roadmap Production

**Version actuelle** : 1.1.0
**État** : Prêt à 85% pour la production
**Note globale** : 8.5/10

---

## 📊 État des lieux

### ✅ Points forts
- Architecture modulaire et claire
- 37 tests unitaires qui passent tous
- Documentation complète (README, CLAUDE.md, CONTRIBUTING)
- Sécurité : protection path traversal
- Configuration persistante fonctionnelle
- Interface multilingue (FR/EN)
- Pre-commit hooks configurés

### ⚠️ Points à améliorer
- app.py trop monolithique (1290 lignes)
- Pas d'exécutable autonome
- Couverture de tests incomplète
- Gestion d'erreurs à renforcer
- Documentation utilisateur finale manquante

---

## 🎯 Plan d'action

### 🔴 PRIORITÉ 1 - Critique (Bloquant production)

#### 1. Créer l'exécutable Windows (.exe)

**Objectif** : Permettre aux utilisateurs sans Python d'utiliser l'application

**Outil** : PyInstaller

**Étapes** :
1. Installer PyInstaller dans l'environnement de dev
2. Créer un dossier `assets/` avec l'icône de l'application (icon.ico)
3. Générer un fichier `.spec` de base avec PyInstaller
4. Personnaliser le `.spec` pour inclure :
   - Tous les fichiers statiques Streamlit
   - Les dépendances Plotly et Pillow
   - L'icône Windows
   - Les métadonnées de version
5. Créer un script `scripts/build_exe.py` pour automatiser le build
6. Tester l'exe sur une machine sans Python installé

**Défis spécifiques** :
- Streamlit a des fichiers statiques (JS, CSS) à inclure
- Plotly nécessite des assets supplémentaires
- Pillow a des dépendances binaires
- tkinter pour les dialogues doit être bien configuré

**Livrables** :
- `build/momentkeeper.spec` : Configuration PyInstaller
- `scripts/build_exe.py` : Script de build
- `assets/icon.ico` : Icône Windows
- `dist/MomentKeeper.exe` : Exécutable final

**Temps estimé** : 8-10h

---

#### 2. Refactorer app.py

**Objectif** : Rendre le code maintenable et testable

**Problème** : app.py fait 1290 lignes, trop monolithique

**Solution** : Extraire en modules séparés

**Structure cible** :
```
src/moment_keeper/ui/
├── __init__.py
├── sidebar.py          # Configuration (lignes 172-515 actuelles)
├── utils.py            # selectionner_dossier, save_configuration
└── tabs/
    ├── __init__.py
    ├── home.py         # Onglet accueil
    ├── simulation.py   # Onglet simulation
    ├── organization.py # Onglet organisation
    ├── analytics.py    # Onglet analytics
    ├── insights.py     # Onglet insights
    └── gallery.py      # Onglet galerie
```

**Bénéfices** :
- Maintenabilité accrue
- Tests unitaires possibles par onglet
- Réutilisabilité du code
- Respect du principe de responsabilité unique

**Temps estimé** : 6-8h

---

#### 3. Unifier la gestion de version

**Problème** : Version définie dans 2 endroits différents
- `src/moment_keeper/__init__.py` : `__version__ = "1.1.0"`
- `pyproject.toml` : `version = "1.1.0"`

**Solution** : Source unique de vérité

**Approche** : Utiliser `importlib.metadata` pour lire depuis pyproject.toml

**Fichier à modifier** : `src/moment_keeper/__init__.py`

**Temps estimé** : 30min

---

### 🟠 PRIORITÉ 2 - Important (Qualité production)

#### 4. Augmenter la couverture de tests

**Objectif** : Atteindre 80%+ de couverture sur les modules métier

**Modules à prioriser** :
- `analytics.py` : Seulement 2 tests actuellement
- `translations.py` : Pas de tests
- `cli.py` : Pas de tests pour le launcher
- Fonctions utilitaires de `app.py` (après refactoring)

**Commande pour vérifier** :
```bash
pytest --cov=src/moment_keeper --cov-report=html --cov-report=term-missing
```

**Temps estimé** : 4-6h

---

#### 5. Améliorer la gestion des erreurs

**Objectif** : Erreurs explicites et traçables

**Actions** :
1. Créer des exceptions custom (`MomentKeeperError`, `FileOrganizationError`, `ConfigurationError`)
2. Remplacer les `except Exception` trop larges
3. Ajouter des messages d'erreur contextuels pour l'utilisateur
4. Implémenter des fallbacks quand possible

**Fichiers concernés** :
- `app.py` : Ligne 630-646 (try/except trop large)
- `organizer.py` : Ligne 130 (exception générique)
- `config_manager.py` : Ligne 103 (pas de fallback)

**Temps estimé** : 3-4h

---

#### 6. Configurer le logging pour l'exe

**Problème** : En mode exe, les logs console ne sont pas visibles

**Solution** : Activer automatiquement le logging fichier en production

**Emplacement des logs** :
- Windows : `%APPDATA%/momentkeeper/momentkeeper.log`
- macOS : `~/Library/Logs/momentkeeper/momentkeeper.log`
- Linux : `~/.local/share/momentkeeper/momentkeeper.log`

**Fichier à modifier** : `src/moment_keeper/cli.py`

**Temps estimé** : 1-2h

---

### 🟡 PRIORITÉ 3 - Recommandé (Polish production)

#### 7. Documentation utilisateur finale

**Objectif** : Permettre aux utilisateurs non-techniques d'utiliser l'application

**Documents à créer** :
- `docs/USER_GUIDE.md` : Guide utilisateur complet avec captures d'écran
- `docs/INSTALL_EXE.md` : Installation et premier lancement de l'exe
- `docs/TROUBLESHOOTING.md` : Problèmes courants et solutions
- `CHANGELOG.md` : Historique des versions et changements

**Contenu du USER_GUIDE** :
- Présentation de l'application
- Prérequis (format des fichiers, structure attendue)
- Guide pas à pas avec screenshots
- FAQ
- Conseils et bonnes pratiques

**Temps estimé** : 4-5h

---

#### 8. Compléter les type hints

**Objectif** : 100% de type hints pour meilleure maintenabilité

**Fichiers prioritaires** :
- `app.py` : Beaucoup de fonctions sans hints
- `analytics.py` : Quelques fonctions incomplètes

**Outils** : mypy pour validation

**Temps estimé** : 2-3h

---

#### 9. CI/CD avec GitHub Actions

**Objectif** : Automatiser tests et builds

**Workflows à créer** :
- `.github/workflows/ci.yml` : Tests automatiques sur chaque push/PR
- `.github/workflows/release.yml` : Build exe automatique sur tag
- `.github/workflows/lint.yml` : Vérification qualité du code

**Bénéfices** :
- Détection précoce des bugs
- Build reproductibles
- Distribution automatisée

**Temps estimé** : 3-4h

---

## 📋 Checklist de production finale

### Code & Architecture
- [ ] Refactorer app.py en modules UI
- [ ] Créer exceptions custom
- [ ] Compléter les type hints
- [ ] Améliorer gestion d'erreurs globale
- [ ] Unifier la gestion de version

### Tests & Qualité
- [ ] Atteindre 80%+ couverture de tests
- [ ] Ajouter tests pour analytics.py
- [ ] Ajouter tests pour CLI
- [ ] Tester sur Windows 10 & 11
- [ ] Tester avec 10,000+ fichiers

### Documentation
- [ ] Créer USER_GUIDE.md
- [ ] Créer INSTALL_EXE.md
- [ ] Créer TROUBLESHOOTING.md
- [ ] Créer CHANGELOG.md
- [ ] Mettre à jour README avec lien vers l'exe

### Packaging & Distribution
- [ ] Créer momentkeeper.spec optimisé
- [ ] Créer script build_exe.py
- [ ] Créer assets/icon.ico
- [ ] Build et tester l'exe
- [ ] Valider sur machine vierge (sans Python)
- [ ] Créer GitHub Release avec exe

### Sécurité & Conformité
- [ ] Vérifier license headers
- [ ] Scanner dépendances (pip-audit)
- [ ] Scanner l'exe avec antivirus
- [ ] Tester permissions Windows
- [ ] Confirmer RGPD (données 100% locales)

### Optionnel
- [ ] Créer installer Inno Setup
- [ ] Signer l'exe (certificat code signing)
- [ ] Créer version macOS/Linux
- [ ] Ajouter analytics anonymes d'usage

---

## ⏱️ Estimation temps total

| Priorité | Tâches | Temps estimé |
|----------|--------|--------------|
| 🔴 P1 | Exe + Refactoring + Version | 15-19h |
| 🟠 P2 | Tests + Erreurs + Logs | 8-12h |
| 🟡 P3 | Docs + Hints + CI/CD | 9-12h |
| **TOTAL** | **Version production complète** | **32-43h** |

**Version minimale viable** (P1 uniquement) : **15-19h**

---

## 🎯 Stratégie de déploiement

### Phase 1 : MVP Production (P1)
- Créer l'exe fonctionnel
- Refactorer le code pour la maintenabilité
- Unifier la gestion de version
- **Livrable** : Exe Windows téléchargeable

### Phase 2 : Qualité Production (P2)
- Augmenter couverture tests
- Améliorer gestion erreurs
- Configurer logs production
- **Livrable** : Application robuste et traçable

### Phase 3 : Excellence Production (P3)
- Documentation utilisateur complète
- Type hints 100%
- CI/CD automatisé
- **Livrable** : Projet open-source professionnel

---

## 📝 Notes importantes

### Format des noms de fichiers
- ✅ `YYYYMMDD_description.jpg` (supporté)
- ❌ `YYYY-MM-DD_photo.jpg` (non supporté)
- ❌ `photo_YYYYMMDD.jpg` (non supporté)

### Limitations connues
- Date extraite du nom de fichier uniquement (pas EXIF)
- Nécessite Python 3.9+ si exécuté en mode dev
- Exe Windows uniquement (Linux/macOS nécessite build séparé)

### Configuration système
- Windows : `%APPDATA%\momentkeeper\`
- macOS : `~/Library/Application Support/momentkeeper/`
- Linux : `~/.config/momentkeeper/`

---

## 🔄 Prochaines étapes suggérées

1. **Immédiat** : Créer l'exécutable (P1.1)
2. **Court terme** : Refactorer app.py (P1.2)
3. **Moyen terme** : Augmenter tests (P2.1)
4. **Long terme** : CI/CD et automation (P3.3)

---

**Dernière mise à jour** : 2025-01-19
**Auteur** : Évaluation Claude Code
