# Test Data - MomentKeeper 🦖

Ce dossier contient des données de test pour MomentKeeper.

## 📁 Structure

```
test-data/
├── photos/           # Placez vos photos de test ici
│   ├── 20240615_premier_sourire.jpg
│   ├── 20240627_bain_rigolo.jpg
│   ├── 20240715_tient_sa_tete.jpg
│   └── ...
└── README.md        # Ce fichier
```

## 📸 Comment Préparer vos Photos de Test

### 1. Téléchargez des photos libres de droits

Suggestions de sites :
- [Unsplash](https://unsplash.com/s/photos/baby) - Photos de bébés gratuites
- [Pexels](https://www.pexels.com/search/baby/) - Photos de qualité
- [Pixabay](https://pixabay.com/images/search/baby/) - Large sélection

### 2. Renommez vos photos au format requis

**Format obligatoire :** `YYYYMMDD_description.jpg`

#### ✅ Exemples de noms corrects :
```
20240615_premier_sourire.jpg        # Naissance: 15 juin 2024
20240620_dodo_paisible.jpg          # 5 jours après
20240627_bain_rigolo.jpg            # 12 jours après
20240710_premiers_gazouillements.jpg # ~1 mois
20240715_tient_sa_tete.jpg          # ~1 mois
20240815_assit_seul.jpg             # ~2 mois
20240915_mange_tout_seul.jpg        # ~3 mois
20241015_crawling_everywhere.jpg    # ~4 mois
```

#### ❌ Noms qui seront ignorés :
```
2024-06-15_photo.jpg                # Tirets non supportés
photo_20240615.jpg                  # Date à la fin
IMG_20240615_123456.jpg             # Préfixe IMG
bebe_mignon.jpg                     # Pas de date
```

### 3. Scénario de test recommandé

Pour bien tester MomentKeeper, utilisez ce scénario :

**Date de naissance du bébé :** `2024-06-15` (15 juin 2024)

**Photos suggérées :**
- **0-1 mois** (15 juin - 15 juillet) : 2-3 photos
- **1-2 mois** (15 juillet - 15 août) : 2-3 photos
- **2-3 mois** (15 août - 15 septembre) : 2-3 photos
- **3+ mois** (septembre+) : 1-2 photos

## 🚀 Utilisation

### Avec l'interface Streamlit

1. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

2. Configuration dans la sidebar :
   - **Dossier principal :** `C:/path/to/moment-keeper/test-data`
   - **Sous-dossier photos :** `photos`
   - **Date de naissance :** `2024-06-15`
   - **Type de fichiers :** `📸 Photos uniquement`

3. Allez dans l'onglet **🔍 Simulation** et cliquez sur **🦖 Analyser les photos**

4. Vérifiez le résultat dans l'onglet **📊 Analytics** et **🦖 Insights**

### Avec les scripts de benchmark

```bash
# Tester les performances sur vos données
python scripts/benchmark.py

# Tester la compatibilité des noms de fichiers
python scripts/test_limits.py
```

## 🎯 Résultats Attendus

Avec le scénario recommandé, vous devriez voir :

- **Dossiers créés :**
  - `0-1months/` - Photos de juin-juillet 2024
  - `1-2months/` - Photos de juillet-août 2024
  - `2-3months/` - Photos d'août-septembre 2024
  - `3-4months/` - Photos de septembre+ 2024

- **Analytics :**
  - Graphiques de répartition par mois
  - Métriques de fréquence de capture
  - Insights sur vos habitudes photo

- **Fichiers ignorés :**
  - Photos avec mauvais format de nom
  - Photos antérieures à la date de naissance

## 💡 Conseils

- **Variété :** Utilisez des photos avec des descriptions différentes
- **Dates réalistes :** Étalez les photos sur plusieurs mois
- **Test de robustesse :** Ajoutez quelques fichiers avec de mauvais noms pour tester la gestion d'erreurs
- **Extensions :** Testez différents formats (.jpg, .jpeg, .png, .heic, .webp)

## 📝 Note importante

**Les photos ne sont PAS stockées dans Git** (voir `.gitignore`). Chaque développeur doit :
1. Télécharger ses propres photos de test
2. Les placer dans `test-data/photos/`
3. Suivre les instructions de nommage ci-dessus

Cela évite de surcharger le repository avec des fichiers binaires volumineux.

## 🆘 Dépannage

Si aucune photo n'est trouvée :
1. Vérifiez le format des noms de fichiers
2. Assurez-vous que les dates sont postérieures à la naissance
3. Vérifiez les extensions de fichiers supportées
4. Consultez la section "Debug" dans l'interface Streamlit

---

*Happy testing! 🦖✨*
