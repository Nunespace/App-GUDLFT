# GÜDLFT : Application de réservation régionale

***
GÜDLFT propose une plateforme numérique pour coordonner les compétitions de force.
Ce projet est une démonstration de faisabilité (proof of concept) d'une version légère de la plateforme pour les organisateurs de compétitions locales et régionales.

## Fonctionnalités de l'application

L'application permettra aux clubs d'inscrire des athlètes aux compétitions organisées au sein de la division. Chaque
compétition aura un nombre limité d'inscriptions, et chaque club ne peut inscrire qu'un maximum de 12 athlètes.
 
## Configuration actuelle

L’application est alimentée par [des fichiers JSON](https://www.tutorialspoint.com/json/json_quick_guide.htm). Il s’agit de contourner le fait d’avoir une base de données jusqu’à ce que nous en ayons vraiment besoin. Les principaux sont les suivants : 
* competitions.json - liste des compétitions
* clubs.json - liste des clubs avec des informations pertinentes. Vous pouvez regarder ici pour voir quelles adresses e-mail l’application acceptera pour la connexion.

## Prérequis

L'application aura besoin de Python, Git et Pipenv pour fonctionner. Si besoin, vous pouvez les installer en suivant les instructions sur [cette page](docs/installation_python-git-pipenv.md).

## Installation

Cette application exécutable localement peut être installée en suivant les étapes décrites ci-dessous.

1. Ouvrez le terminal et tapez :

```
git clone https://github.com/Nunespace/App-GUDLFT.git
```

Vous pouvez également télécharger le dossier en temps qu'archive zip : [Projet_App_GUDLFT .zip](https://github.com/Nunespace/App-GUDLFT/archive/refs/heads/master.zip)

2. Placez-vous dans le répertoire App-GUDLFT :
```
cd App-GUDLFT
```

3. Installez les dépendances du projet :
```
pipenv install
```
 
4. Démarrer le serveur avec : 
```
pipenv run python server.py
```
5. Ouvrez votre navigateur et entrez l’URL suivante : [http://127.0.0.1:5000/](http://127.0.0.1:5000/) comme indiqué sur le terminal pour démarrer l'application.

6. Pour quitter le serveur, appuyez sur ` CTRL+C `

Pour les lancements ultérieurs du serveur, il suffit d'exécuter les étape 4 et 6 à partir du répertoire racine du projet.

## Tests

Les tests de ce projet ont été écrits avec le framework pytest et son plugin pytest-flask.

### Lancement des tests
Les tests sont executables avec la commande : 
```
pipenv run pytest
```

Il est possible de lancer qu'un seul test. Par exemple : 
```
pipenv run pytest tests/unit/test_app.py::TestBookPlaces::test_get_book_page
```

### Rapport HTML

Un rapport html des tests peut être obtenu avec la commande : 
```
pipenv run pytest --html=report.html --self-contained-html
```

Il sera ensuite disponible à cette adresse : 127.0.0.1:5500/report.html


### Couverture de test

Ce projet contient la librairie Python Coverage.py qui fournit un rapport qui nous donne le pourcentage de couverture de ligne par fichier source de couverture. Ce rapport peut être obtenu avec cette commande : 
```
pipenv run pytest --cov=.
```
Un rapport HTML, plus détaillé, peut aussi être généré en tapant : 
```
pipenv run pytest --cov=. --cov-report html
```
Ce dernier est ainsi consultable à cette adresse http://127.0.0.1:5500/htmlcov/index.html


### Performances

Le framework Locust a été utilisé pour réaliser les tests de performance de l'application mesurant les temps de réponse des différentes fonctionnalités (temps de chargement et mises à jour).

Pour exécuter ces tests :

1. Ouvrir un terminal pointant sur le répertoire contenant le fichierlocustfile.py en tapant, à partir de la racine du projet : 
```
cd tests\performance_tests
```

2. Taper :
```
pipenv run locust
```

3. Ouvrez votre navigateur et taper l'adresse : [http://localhost:8089/](http://localhost:8089/)

4. Sur cette page, vous devez préciser :

    - Number of total users to simulate : le nombre total d'utilisateurs à simuler (fixé pour ce projet à six par défaut).

    - Spawn rate : le taux de création d'utilisateurs, il correspond au nombre d’utilisateurs créés par seconde jusqu’à atteindre le nombre total d’utilisateurs. 

    - Host : l’adresse de l'application : http://127.0.0.1:5000 (localhost).

> [!IMPORTANT]
> Lancer l'application au préalable, sinon, toutes les requêtes vont échouer.




