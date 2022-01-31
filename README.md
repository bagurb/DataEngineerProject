# WebScraping NASDAQ Dashboard

## Sommaire
* [Informations Générales](#Informations-Générales)
* [Installation](#Installation)
* [Developper's Guide](#Developper's-Guide)

## Informations Générales

Pour ce projet nous avons choisi de nous intéresser à différentes entreprises concernant la NASDAQ. Les compagnies auxquelles nous nous sommes intéressées sont toutes 
particulièrement influentes dans leur domaines respectifs et de ce fait, scrapper des données les concernant serait particulièrement pertinent pour en sortir des informations.

Durant ce projet , nous avons scrappé différents articles de journaux concernant une dizaine d’entreprises du NASDAQ (bourse américaine). 

Le but étant d'afficher sur un DashBoard certaines caractéristique de l’entreprise:

* Courbe boursière de chaque entreprise.

* Valeur minimal de l’action en bourse.

* Valeur maximal de l’action en bourse.

* Le valeur moyenne de chaque action.

* Un article de journal d’actualité choisi aléatoirement parmis les articles scrappés , ayant un impact bénéfique ou négatif sur la valeur de l’action.


Ces différents éléments nous permettent d’avoir une première approche d’étude sur l'intérêt de ces actions en bourse .
L'intérêt de notre DashBoard est qu’il puisse afficher des données d’actualités dynamiques et récentes concernant chaque action. En effet, ces éléments sont pertinents afin de mieux comprendre la croissance ou décroissance d’une entreprise en bourse.
Ce qui peut attirer ou non de futurs entrepreneurs.

L’actualité boursière est un milieu dense et complexe, c’est pour cela que notre solution permet d'affiner nos recherches et de se concentrer sur les éléments primordiaux.

## Installation

Pour que le programme fonctionne vous devez éxécuter dans un terminal la commande suivante afin d'importer les packages:

```
pip install -r requirements.txt
```
Ensuite il vous suffit de taper la commande suivant dans votre terminal:

```
python main.py
```

Le script de scraping, les fonctions ainsi que le dashboard vont alors s'éxécuter. Lorsque le programme aura terminer de scraper, traiter les donnnées et construire le dashboard, vous pourrez vous rendre à l'addresse suivante: http://127.0.0.1:3000/ afin d'ouvrir le dashBoard.

## Developper's Guide

### Architecture globale

Le projet est découpé en 3 scripts:

* Dans le dossier root (DataEngineerProjet), vous retrouverez le script data_functions.py contenant toutes les fonctions de calcul pour les appels de script, le traitement des données, leurs mise en relation avec la base de données MongoDB, la récupération des données à l'aide des requêtes mongoDB.
* Dans ce même dossier, le script main, s'appuie sur les fonctions de data_functions.py pour lancer le script de scraping, créer la base de donnée MongoDB, créer le dashboard et traiter la mise en page de celui-ci.
* Un dernier script article_spider.py contenu dans le dossier nasdaq/spiders s'occuppe de la récupération des articles de journaux par la méthode de scraping. Une liste d'url contenu dans le dossier nasdaq/spiders/urls permet de récupérer de nombreux articles automatiquement sur plusieurs sites.

### Récupération des données

* Pour les datas

Pour les données boursières, nous avons dû télécharger séparément les csv des entreprises sur le site du Nasdaq car nous n'avons pas réussi à scraper les données directement depuis les tableaux. En effet, nous penssons que ces tableaux sont protégés contre le scraping et n'avions plus vraiment de temps pour trouver une solution. Nous avons également essayer de monter une fonction téléchargeant automatiquement les csv afin de garder des données dynamiques. Cependant, le téléchargement des csv est lui aussi protégé sur le site du NASDAQ et ne nous offre aucune URL récupérable afin d'automatiser le processus. La dernière alternative que nous n'avons pas pu mettre en place faute de temps, aurait été d'utiliser l'API du NASDAQ afin de récupérer leurs données.
Pour le traitement des données, nous avons donc choisi d'ajouter une colonne "Société" avec le nom des entreprises pour chaque observation afin de fusionner tout les csv en un csv unique nommé data.csv. Nous avons ensuite effectué des conversions en numeric et datetime afin de pouvoir utiliser ces données dans notre dashboard. Une fois les données nettoyées et traitées, nous avons importer ce csv dans une base de données MongoDB pour faciliter l'utilisation de celle-ci.

* Pour les articles

Les articles sont scrappés à partir d'une liste d'url, ils sont ensuite stockés dans un fichier .json: Datas/articles.json. Pour chaque article nous récupérons son titre en brute, son texte en brute,l'URL ainsi que le nom de la société à laquel l'article est associé. Nous avons décider de traiter ses articles afin de retirer les caractères spéciaux qui les rendent illisibles tout en concervant les apostrophes et autres caractères de ponctuation. Une fois le traitement effectué, nous stockons les articles sur une collection MongoDB afin de les utiliser plus tard.

### Utilisation des données et composition du DashBoard

Les données sont utilisées afin de mettre en place un dashboard qui centraliserait ces dernières. Le dashboard est composé de 11 pages :
* 1 page d'accueil avec les graphiques sur 1 an de toutes les entreprises séléctionnées ainsi que des informations sur le min,max et moyenne du cours de leurs actions.
* 10 pages spécifiques à chaque entreprise avec le graphiques, les informations min,max,average, un tableau de donnée et un article récent aléatoire avec le lien de l'article.

Les données sont utiliser à l'aide de requête mongoDB afin de retourner les x et y nécessaire à la création des graphiques. D'autres requêtes permettent de récupérer l'ensemble des données afin de créer le tableau mais également pour tirer le min, max et average des données.
Enfin des requêtes sur la collection d'article permettent de sortir un article aléatoire sur l'entreprise en récupérant son titre, le texte ainsi que le lien.

