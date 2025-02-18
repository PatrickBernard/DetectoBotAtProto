# DetectoBotAtProto

Simplifier la recherche de compte de l'opération doppelganger

## Intro

Tentative de simplifier la recherche de compte de l'opération doppelganger

## Méthodologie

- retrouver les messages d'un bot
  - connection ok
  - récupération des posts de la cible ok
  - stockage de maniere unique pour limiter le nombre de requetes
    - une base de donnée (sqlite) avec une clef basé sur le md5 du texte fera l'affaire.
- faire une recherche sur ce message
  - enregistrer les comptes detectés avec une clef md5 pour eviter les doublons

## Todo
- remplir automatiquement une liste de modération
- mettre plus de paramettre plutot que de la config en dur
- ...

## Prérequis d'installation

``pipx install atproto``

## usage :

- ``cp sample-settings.ini settings.ini``
- remplir le settings.ini
- il vous faudra un compte bot cible pour initier la recherche
- ``python detectobotatproto.py``

## a propos de la base sample-doppelganger.db
- contient :
  - messages de bot russe
  - comptes ayant été ban par la modération 
- Vous pouvez l'utiliser en la recopiant ``cp sample-doppelganger.db botmessage.db``
