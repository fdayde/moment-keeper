# 🦖 Photos de test MomentKeeper

Ce dossier contient des photos de démonstration pour tester MomentKeeper sans utiliser vos propres photos.

## 📁 Structure du dossier de démo

```
data/test/                 # Dossier racine de la démo
└── photos/                # Dossier source contenant les photos
    ├── 20240701_275-4288x2848.jpg
    ├── 20240705_237-3500x2095.jpg
    ├── 20240901_219-5000x3333.jpg
    └── 20241101_200-1920x1280.jpg
```

## 📸 Contenu

4 photos de test avec des dates différentes :
- `20240701_275-4288x2848.jpg` - 1er juillet 2024 (bébé de 1 mois)
- `20240705_237-3500x2095.jpg` - 5 juillet 2024 (bébé de 1 mois)
- `20240901_219-5000x3333.jpg` - 1er septembre 2024 (bébé de 3 mois)
- `20241101_200-1920x1280.jpg` - 1er novembre 2024 (bébé de 5 mois)

## 🎯 Utilisation

1. Lancez l'application : `streamlit run app.py`
2. Cliquez sur **"Charger config test"** dans la barre latérale
3. La configuration sera automatiquement chargée :
   - Dossier racine : `data/test` (relatif au projet)
   - Dossier source : `photos` (relatif au dossier racine)
   - Prénom : TestRex 🦖
   - Date de naissance : 1er juin 2024
   - Les photos seront organisées en 3 dossiers : 1-2months, 3-4months, 5-6months

## 📁 Organisation attendue

Après organisation, les photos seront déplacées de `data/test/photos/` vers `data/test/` :
```
data/test/
├── photos/                # Dossier source (vide après organisation)
├── 1-2months/
│   ├── 20240701_275-4288x2848.jpg
│   └── 20240705_237-3500x2095.jpg
├── 3-4months/
│   └── 20240901_219-5000x3333.jpg
└── 5-6months/
    └── 20241101_200-1920x1280.jpg
```

## ✨ Avantages de cette structure

- **Portable** : Fonctionne sur tous les systèmes (Windows, Mac, Linux)
- **Chemin relatif** : Pas de chemin en dur, s'adapte à chaque installation
- **Isolation** : La démo est isolée dans son propre dossier
- **Réinitialisation facile** : Le bouton "Réinitialiser" remet tout en place

## ℹ️ Note

Ces photos sont versionnées dans Git pour permettre à tous les utilisateurs de tester l'application immédiatement.
