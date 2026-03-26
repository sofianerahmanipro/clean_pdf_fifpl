# Fix PDF Font Size

## Table des matières

- [Description](#description)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [➡️ Utilisation](#utilisation)
- [Fonctionnement](#fonctionnement)
- [Options](#options)
- [Limitations](#limitations)

## Description

Ce script Python permet de corriger les tailles de police dans les champs de formulaire d'un fichier PDF. Il est particulièrement utile pour les PDFs générés par certains logiciels qui définissent des tailles de police à 0, rendant le texte invisible ou mal affiché.

Le script utilise la bibliothèque `pikepdf` pour manipuler les PDFs et corrige automatiquement :
- Les tailles de police nulles (0) en les remplaçant par une taille par défaut (10).
- Supprime les apparences (/AP) pour les champs contenant des balises.
- Active l'option `/NeedAppearances` pour forcer la régénération des apparences.

## Prérequis

- Python 3.6 ou supérieur (testé avec Python 3.11.15 dans un environnement virtuel)
- Bibliothèque `pikepdf` (installable via pip)

## Installation

1. Clonez ou téléchargez ce dépôt.
2. Installez les dépendances :

   ```bash
   pip install pikepdf
   ```

## Utilisation

Exécutez le script en ligne de commande en passant le chemin du fichier PDF en argument :

```bash
python fix_pdf_font_size.py "chemin/vers/votre/fichier.pdf"
```

Le script générera un nouveau fichier PDF avec le suffixe "_fixed" dans le même répertoire.

### Exemple

```bash
python fix_pdf_font_size.py "Attestation FIFPL Présentiel — Base Tout Public.pdf"
```

Cela produira un fichier `Attestation FIFPL Présentiel — Base Tout Public_fixed.pdf`.

## Fonctionnement

Le script analyse le formulaire AcroForm du PDF :
- Recherche les champs contenant des balises (définies par des expressions régulières comme `{.*}`).
- Pour ces champs, corrige les propriétés `/DA` (apparence par défaut) en remplaçant les tailles de police 0 par 10.
- Supprime les propriétés `/AP` (apparences) pour éviter les conflits.
- Répète le processus pour les widgets enfants.
- Active `/NeedAppearances` pour s'assurer que les apparences sont régénérées correctement.

## Options

Actuellement, le script utilise une taille de police par défaut de 10. Pour modifier cette valeur, éditez la ligne `total += fix_field(field, 10, False)` dans la fonction `main()`.

Le paramètre `dry_run` est défini à `False` pour appliquer les modifications. Pour un mode test (sans modification), changez-le à `True`.

## Limitations

- Le script ne modifie que les PDFs contenant un formulaire AcroForm.
- Il suppose que les tailles de police sont spécifiées dans le format `/FontName 0 Tf`.
- Pour des PDFs complexes, vérifiez toujours le résultat.
