# DetectoBotAtProto  

Simplification de la recherche de comptes dans l'opération Doppelgänger  

## Introduction  

Tentative de simplifier la recherche de comptes dans l'opération Doppelgänger.  

## Méthodologie  

- Retrouver les messages d'un bot :  
  - Connexion : OK  
  - Récupération des posts de la cible : OK  
  - Stockage de manière unique pour limiter le nombre de requêtes :  
    - Une base de données (SQLite) avec une clé basée sur le MD5 du texte suffira.  
- Effectuer une recherche sur ce message.  
  - Enregistrer les comptes détectés avec une clé MD5 pour éviter les doublons.  

## À faire  

- Remplir automatiquement une liste de modération.  
- Ajouter plus de paramètres au lieu d'avoir une configuration en dur.  
- ...  

## Prérequis d'installation  

```bash
pipx install atproto
```  

## Utilisation  

1. Copier le fichier de configuration exemple :  
   ```bash
   cp sample-settings.ini settings.ini
   ```  
2. Remplir le fichier `settings.ini`.  
3. Un compte bot cible sera nécessaire pour initier la recherche.  
4. Lancer le script :  
   ```bash
   python detectobotatproto.py
   ```  

## À propos de la base `sample-doppelganger.db`  

- Contient :  
  - Des messages de bots russes.  
  - Des comptes ayant été bannis par la modération.
    - peu interessant car souvent ban
- Vous pouvez l'utiliser en la recopiant :  
  ```bash
  cp sample-doppelganger.db botmessage.db
  ```  
