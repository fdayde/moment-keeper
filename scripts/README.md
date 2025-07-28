# Scripts de Performance et Tests

## 📊 Benchmark des Performances

```bash
# Installer les dépendances supplémentaires
pip install psutil

# Lancer le benchmark complet
python scripts/benchmark.py
```

Ce script va :
- Créer des collections de 100 à 10,000 fichiers
- Mesurer le temps de traitement
- Monitorer l'utilisation mémoire
- Calculer les fichiers/minute
- Générer un rapport de performance

## 🧪 Test des Limitations

```bash
# Tester les limitations système
python scripts/test_limits.py
```

Ce script va :
- Tester différents formats de noms de fichiers
- Évaluer la gestion de fichiers volumineux
- Vérifier la compatibilité multiplateforme
- Générer un rapport des limitations

## 📈 Utilisation des Résultats

Après avoir lancé les benchmarks :

1. **Performances** : Utilisez les métriques pour documenter la section Performance du README
2. **Limitations** : Documentez les contraintes identifiées
3. **Compatibilité** : Listez les OS testés avec succès

## Exemple de sortie benchmark :

```
📈 RÉSUMÉ DES PERFORMANCES
==================================================
   100 fichiers |   0.45s |    133 fichiers/min |   45.2 MB
   500 fichiers |   1.82s |    165 fichiers/min |   52.1 MB
  1000 fichiers |   3.21s |    187 fichiers/min |   68.3 MB
  2000 fichiers |   6.45s |    186 fichiers/min |   89.7 MB
  5000 fichiers |  15.32s |    196 fichiers/min |  145.2 MB
 10000 fichiers |  29.87s |    201 fichiers/min |  234.5 MB

🏆 MÉTRIQUES FINALES
   • Testé jusqu'à: 10000 fichiers
   • Vitesse moyenne: ~180 fichiers/minute
   • Mémoire maximale: 235 MB
   • Efficacité: ✅ Stable sur toutes les tailles
```
