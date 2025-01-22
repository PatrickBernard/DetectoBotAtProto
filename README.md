# DetectoBotAtProto

Simplifier la recherche de compte de l'opération doppelganger

## Intro

Tentative de simplifier la recherche de compte de l'opération doppelganger

## Méthode / todo

1 - retrouver les messages d'un bot
    - connection ok
    - récupération des posts de la cible ok
    - stockage de maniere unique pour limiter le nombre de requetes
      - une base de donnée (sqlite) avec une clef basé sur le md5 du texte fera l'affaire.

2 - faire une recherche sur ce message

3 - afficher le résultat

4 - ajouter/faire une liste de modération

## Prérequis

``pipx install atproto``
