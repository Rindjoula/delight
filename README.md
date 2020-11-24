# Généralités
Pour chaque script python ci-dessous, il faut passer en paramètre un token d'authentification afin de télécharger les données via l'API REST. Ce token peut être généré via Github. 

## Contributeurs

* Exécuter le script *contributor.py* avec en paramètre le token d'authentification
* Résultats: écriture de tous les contributeurs dans le fichier *contributors.json*

## Liste des commits journaliers

* Exécuter le script *dailyCommits.py* en décommentant la ligne "write_commits_per_year(token, 2020)" dans le main
* Résultats: écriture de tous les commits de chaque jour en 2020 (jusqu'à maintenant, avec un fichier par jour)

* Pour récupérer les jours critiques où on a moins de deux commits, il faut décommenter la ligne "get_critical_days" dans le main. 
* Résultats: les jours critiques sont stockés dans le fichier *critical_days.json* alors créé

## Visualisation
* En décommentant la ligne "visualize_contributions()" dans le main, on obtient la figure *contributons.png* contenant un diagramme circulaire avec le nombre de contributions par contributeur non anonyme ayant fait plus de 300 commits. On a également les pourcentages des contributions des anonymes, des bots et des utilisateurs ayant fait moins de 300 commits. 

## Améliorations possibles et difficultés rencontrées

* Je ne sais pas si écrire un fichier par commit est la meilleure optimisation. J'ai fait ce choix pour deux raisons principales. Premièrement, cela me semblant plus simple pour ensuite récupérer les jours critiques. Si les commits étaient stockés (par exemple) par mois, quand on récupère les commits d'un mois entier, il faudrait ensuite les diviser. Par ailleurs, je n'ai ici récupéré que les commits de la branche principale "master", ce qui fait qu'il n'y a que peu de commits par jour. On peut imaginer récupérer les commits de plus de branches, et on pourrait avoir alors beaucoup plus de commits par jour. Les stocker par jour me semble alors pertinent. 

* Comme dit précédemment, je n'ai récupéré que les commits de la branche master. En effet, je n'ai pas trouvé de moyen réellement optimisé pour récupérer la totalité de tous les commits sur toutes les branches, sachant qu'il y a 201 branches (récupérées et écrites dans un fichier json *branches.json* grâce au script *branch.py*), toutes ne sont pas forcément actives et l'API ne permet de faire que 5000 requests par heure. 

* Concernant la visualisation, je n'ai pas compris ce qui était attendu dans le plot "log-log". 