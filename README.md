# FootballPLayer_recommendation_system

Le projet a été réalisé par Charlie Martin et Suvin Sasikumar

Le projet se décompose en 3 étapes:
1) Le notebook "Scrapping_transfermarkt.ipynb" permet de scrapper les données du site transfermarket : https://www.transfermarkt.fr/wettbewerbe/europa, et permet de retourner un premier dataset avec 3k joueurs et leurs informations issus du site web. On part de  ce dataset pour scrapper les données du deuxième site web, ci dessous. 
2) Le notebook "Scrappig_Football_observatory.ipynb" permet de 
    - scrapper les données du site football observatory : https://football-observatory.com/IMG/sites/playerprofile/
    - mettre en place notre modèle de recommendation de joueurs 
3) Le dossier "Interface WEB & API" permet de créer notre interface web grâce à Fastapi. Il faut télécharger le dossier en entier.
  - le fichier main.py permet de lancer l'interface web. Il faut lancer la requete : ...
  - le dossier templates, regroupe les codes html de la page web 
 

Vous retrouverez la présentation du projet, dans le fichier "Presentation project.pdf"
