# ⚙️ Configuration de test MomentKeeper

Ce dossier contient la configuration de démonstration pour tester MomentKeeper.

## 🎯 Utilisation rapide

1. Lancez l'application : `streamlit run app.py`
2. Cliquez sur **"Charger config test"** dans la sidebar
3. Tout est prêt ! 🦖

## 📝 Configuration de la démo (`test_config.json`)

```json
{
  "dossier_path": "data/test",        // Chemin relatif au projet
  "sous_dossier_photos": "photos",     // Dossier source des photos
  "language": "fr",                    // Interface en français
  "baby_name": "TestRex",              // Prénom du bébé T-Rex
  "photos_selected": true,             // Photos activées
  "videos_selected": true,             // Vidéos activées
  "date_naissance": "2024-06-01"       // Né le 1er juin 2024
}
```

## ✨ Avantages

- **Portable** : Chemins relatifs, fonctionne partout
- **Prêt à l'emploi** : Un clic et c'est parti
- **Sans risque** : Vos vraies photos restent intactes
- **Réversible** : Bouton "Réinitialiser" disponible

## 📸 Photos de test

Voir `data/test/README.md` pour la liste des photos disponibles.
