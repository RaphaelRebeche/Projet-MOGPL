# Projet-MOGPL

## Introduction
Le rendu comporte trois fichiers python distinct.
- <code>main.py</code> comporte le programme nécessaire à la mise en place d'un interface demandé en question (e).
- <code>utils.py</code> comporte toutes les fonctions nécessaires à la réponse aux questions (a) à (d).
- <code>PL.py</code> comporte les fonctions nécessaires à la résolution du PL de la question e.

## main.py
- Se lance en rentrant dans un terminal <code>python(3) {path}/main.py m n p</code><br>
Où <code>m</code>,<code>n</code> et <code>p</code> sont des entiers représentant le nombre de lignes, de colonnes et d'obstacles. Si le modèle est validé par le solveur, il vous sera demandé de rentrer 5 autres arguments <code>dx</code>, <code>dy</code>, <code>o</code>, <code>fx</code> et <code>fy</code>, séparés eux aussi par des espaces, où <code>dx</code>, <code>dy</code>, <code>fx</code> et <code>fy</code> sont des entiers représentant les lignes et les colonnes des poits de début et de fin et <code>o</code> une chaîne de caracère représentant un point cardinal (nord, ouest, sud, est, n, o, s, e et leurs variantes avec des majuscules sont également acceptées).<br>
Si au moins un des deux points n'est pas accessibles dans aucunes des <code>n</code> solutions renvoyées par le solveur il est demandé de réessayer avec d'autres coordonnées (dans certains cas, trouver deux points accessibles peut s'avérer fastidieux).

## utils.py
- Les fonctions is_accessible et create_accessibility_matrix permettent de déterminer, à partir d'une matrice d'obstable, si un point est accessible et d'en déduire la matrice d'accessibilité<br>

- La fonction create_random_matrix_start_end permet de créer : une matrice comportant des 0 et des 1 qui modélisent l'absence où la présence d'un obstacle, un point start (ligne, colonne et orientation), un point end (ligne colonne). Chacune de ces matrices ou vecteurs est généré aléatoirement.<br>
  

- Les fonctions append_matrix_to_file et create_file_test permettent de créer un fichier au format de l'énoncé.<br>
append_matrix_to_file prend en paramètre une matrice (correspondant aux obstacles), un vecteur (où on retrouve le point start, son orientation et le point end) et le nom du fichier dans lequel cette matrice et le vecteur associé seront écrit.<br>

- La fonction read_matrix permet la lecture d'un fichier au format de l'énoncé en d'en extraire une liste où chaque ligne correspond à une matrice, le point de départ à d'arrivé qui lui sont associées.<br>

- La fonction create_adjacency_dictionnary permet de créer un dictionnaire dans lequel chaque clé correspond à un noeud du graphe et chaque valeur associée est une liste avec toutes les arêtes vers lequel va ce noeud. La fonction dijkstra parcours le graphe que ce dictionnaire modélise et détermine le plus cours chemin entre le point start et tous les points de la matrice, elle renvoie le temps en seconde du trajet le plus cours, ainsi que la succession de noeud pour y arriver. (C'est donc 2 output, un avec la matrice et tous les éléments, un vecteur avec le temps et le trajet)<br>

- Les fonctions get_path_to et get_path_textual permettent de retracer le chemin le plus cours entre le start et l'end trouvé par dijkstra. get_path_to renvoie les indexs des noeuds par lesquels passe le plus court chemin, get_path_textual permet de déterminer le chemin au format demandé.<br>

- La fonction get_time_iter permet de chronométrer le temps d'execution du code et de récupérer les chemins associés à chacune des matrices, et la fonction draw_boxplot permet d'afficher les boxplots de N en fonction du temps d'exécution.<br>

- La fonction create_output_file permet de créer le fichier de sorti au format demandé<br>

## PL.py
- la fonction create_model permet de résoudre le programme linéraire donné via gurobi<br>
- fonction gen_matrix génère la matrice de 0 et de 1 en fonction du résultat donné par la résolution du programme linéaire<br>
