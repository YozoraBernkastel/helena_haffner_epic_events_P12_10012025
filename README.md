# helena_haffner_epic_events_P12_10012025

## Lancement du programme (environnement virtuel activé)

```shell
 python3 main.py
```

## Description du programme

Programme CRM (Customer Relationship Management) utilisant l'interface du terminal destiné à stocker et manipuler les
informations de clients, de contrats et d'événements s'inscrivant dans le cadre d'une formation Open Classroom.
Ce logiciel est à destination d'une entreprise d'événementiel et permet de garder une trace dans une base de données
SQLite
de ses clients, de ses contrats et des événements dont ses employés ont la charge.

Ce programme utilise une authentification avec une fonctionnalité permettant de se souvenir du dernier utilisateur.
Il y a trois types d'utilisateurs : les managers, les commerciaux et le support. Chaque rôle a des droits différents.

__Bien que Poetry soit l'environnement virtuel utilisé pour le développement, un fichier **requirements.txt** est
présent
dans les fichiers pour ceux ne souhaitant pas utiliser Poetry.__

## Environnement Virtuel

Environnement Virtuel utilisé : Poetry

Installation:

```shell
 curl -sSL https://install.python-poetry.org | python3 - 
```

Activer l'environnement virtuel :
Si la version de votre Poetry est inférieure à 2.1 :

```shell
 poetry shell
```

Si vous utilisez la version 2.1, il faudra soit d'abord installer la commande shell via la commande :

```shell
 poetry self add poetry-plugin-shell
```

Soit utiliser la commande :

```shell
 eval $(poetry env activate)
```

Installer les dépendances (les fichiers pyproject.toml ou poetry.lock doivent être présents dans le dossier et qui sont
l'équivalent de requirements.txt) :

```shell
 poetry install 
```

Sortir de l'environnement virtuel :

```shell
 exit
```

## Lancer le programme sans activer l'environnement virtuel (mais celui-ci doit être installé)

Dans le terminal, à la racine du projet :

```shell
 poetry run python3 main.py
```

## Mettre en place Sentry

Créer un projet Sentry et copier la clé dsn affichée lors de la configuration puis,
dans __main.py__, soit remplacer __os.environ.get("SENTRY_KEY")__ utilisé en argument de la
fonction __sentry_sdk.init()__ par le dsn copié -- *auquel cas, il faudra enlever __if
os.environ.get("SENTRY_KEY")__ du code* -- soit mettre en place la variable d'environnement
__SENTRY_KEY__ en lui attribuant la clé dsn en tant que valeur.

## Tests unitaires

Les tests unitaires ont été écrits en utilisant Pytest.

Pour les lancer, une fois l'environnement virtuel activé, utilisez la commande :

```shell
 pytest
 ```

In est également possible d'utiliser la library Coverage.
Pour cela, utilisez la commande :

```shell
 coverage run -m pytest
 ```

Ensuite, pour voir le taux de couverture, entrez la commande :

```shell
 coverage html
```

Et cliquez sur le lien qui s'affiche dans le terminal.




