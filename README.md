# Voice Waze

## Présentation

Ce projet regroupe des outils permettant de préparer et de gérer des packs de voix personnalisés pour Waze.

Une fonctionnalité développée permet notamment de préparer localement des packs MP3 afin de respecter les contraintes de taille imposées par Waze.

**Important :** la préparation locale ne publie aucun fichier sur les serveurs Waze.

---

## 1. Préparation locale des packs MP3

Le script `waze-voicepack-links/prepare_local_pack.py` automatise deux opérations :

1. La validation des fichiers MP3.
2. La compression des packs afin de respecter la limite de taille.

### Fonctionnement

**Étape 1 — Validation**

Le module `mp3_upload/file_ingestion.py` :
- Parcourt les packs présents dans `mp3_upload/input_packs/`.
- Vérifie les noms des fichiers à partir de `valid_waze_filenames.txt`.
- Vérifie l'intégrité des fichiers audio.

Seuls les fichiers correspondant aux noms officiels sont retenus.

**Étape 2 — Compression**

Le module `mp3_upload/file_compression.py` :
- Convertit les fichiers en MP3 mono, 44,1 kHz.
- Ajuste automatiquement le débit binaire lorsque cela est nécessaire.
- Recherche le meilleur débit permettant de respecter la limite de taille.
- Conserve une copie originale des fichiers avant compression.
- Ne supprime pas les sauvegardes originales.

Si la compression échoue, le traitement signale les packs concernés.

---

## 2. Paramètres actuels

| Paramètre | Valeur |
|---|---|
| Taille maximale visée | 0,795 MB |
| Débit maximal | 128 kbps |
| Débit minimal | 16 kbps |
| Fréquence d'échantillonnage | 44 100 Hz |
| Nombre de canaux | 1 (mono) |
| Modification du volume | 0 dB |

Le volume est volontairement conservé à son niveau d'origine afin d'éviter une amplification excessive et une dégradation inutile du son.

---

## 3. Organisation des fichiers

Dans le dépôt `waze-voicepack-links` :

- `prepare_local_pack.py` : point d'entrée de la préparation locale.
- `mp3_upload/input_packs/` : emplacement des packs sources.
- `mp3_upload/compressed_packs/` : résultats de la compression.
- `mp3_upload/valid_waze_filenames.txt` : liste des noms de fichiers acceptés.

Le dossier `compressed_packs` contient :
- Les packs compressés.
- Les copies originales utilisées pour la compression, dans les dossiers suffixés `__ORIGINAL`.
- Les archives originales sont conservées dans `zip-origine/` à la racine du projet.
- Les packs validés sont conservés localement dans `outputs/`, qui est ignoré par Git.

Les dossiers de sauvegarde et les fichiers générés ne doivent pas être ajoutés inutilement à Git.

---

## 4. Installation et exécution

Le projet utilise un environnement virtuel Python situé à la racine de `voice-waze` :

`.venv/`

FFmpeg et FFprobe sont installés localement dans :

`tools/ffmpeg/ffmpeg-9.1-essentials_build/bin/`

Le script configure automatiquement leur emplacement.

Depuis PowerShell, à la racine de `voice-waze` :

```powershell
.\.venv\Scripts\python.exe .\waze-voicepack-links\prepare_local_pack.py
```

Avant chaque nouvelle préparation :
- Placer les packs à traiter dans `mp3_upload/input_packs/`.
- Vérifier que le dossier `compressed_packs/` n'existe pas déjà.
- Si des résultats précédents doivent être conservés, les déplacer ou les renommer avant de relancer le traitement.

Le script refuse volontairement d'écraser un dossier de résultats existant.

---

## 5. Versions validées

Les essais réalisés le 25 novembre 2026 ont permis de valider :

- **Ado-Rebelle** : deuxième version validée, sans amplification du volume.
- **C3-PO** : compression validée, sans amplification du volume.

Aucune publication sur Waze n'a été effectuée.

---

## 6. Précautions importantes

- Ne jamais modifier les fichiers sources originaux pour effectuer une compression.
- Conserver les sauvegardes avant toute nouvelle opération.
- Ne pas supprimer les dossiers `__ORIGINAL` sans avoir vérifié les résultats.
- Ne pas lancer les scripts d'envoi vers Waze pour une simple préparation locale.
- Vérifier le résultat audio à l'écoute avant de valider définitivement un pack.

---

## 7. Gestion du code avec Git

Le développement de la préparation locale a été effectué sur la branche :

`preparation-locale-mp3`

Le travail réalisé le 25 novembre 2026 a été enregistré dans un commit local.

La structure Git du projet doit encore être simplifiée : le dépôt parent `voice-waze` et le dépôt imbriqué `waze-voicepack-links` sont actuellement indépendants.

Une migration vers un dépôt unique à la racine est envisagée, avec conservation de l'historique original et de la possibilité de récupérer les futures modifications du projet d'origine.

**Ne pas effectuer cette migration sans avoir préalablement sauvegardé et vérifié les deux dépôts.**
