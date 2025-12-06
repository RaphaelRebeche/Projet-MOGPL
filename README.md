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
is_accessible prend en paramètre i, j et M c'est à dire la ligne et la colonne du point d'intéret sur la matrice M<br>
create_accessibility_matrix prend en paramètre une matrice M et à partir de celle-ci, en utilisant is_accessible, créer une matrice d'accessibilité.  

- La fonction create_random_matrix_start_end permet de créer : une matrice comportant des 0 et des 1 qui modélisent l'absence où la présence d'un obstacle, un point start (ligne, colonne et orientation), un point end (ligne colonne). Chacune de ces matrices ou vecteurs est généré aléatoirement.<br>
create_random_matrix_start_end prend en paramètre N et P_obstacle. Si P_obstacle = True alors N correspond au nombre d'obstacles dans la matrice, si P_obstacle = False alors N correspond à la taille d'un côté de la matrice.  

- Les fonctions append_matrix_to_file et create_file_test permettent de créer un fichier au format de l'énoncé.<br>
append_matrix_to_file prend en paramètre une matrice (correspondant aux obstacles), un vecteur (où on retrouve le point start, son orientation et le point end) et le nom du fichier dans lequel cette matrice et le vecteur associé seront écrit.<br>
create_file_test prend en paramètre obstacle. Si obstacle = False alors il créer un fichier permettant de réaliser les tests demander dans la question c, si obstacle = True alors il créer un fichier permettant de réaliser les tests demander dans la question d.  

- La fonction read_matrix permet la lecture d'un fichier au format de l'énoncé en d'en extraire une liste où chaque ligne correspond à une matrice, le point de départ à d'arrivé qui lui sont associées.<br>
read_matrix prend en paramètre le nom du fichier à lire  

- La fonction create_adjacency_dictionnary permet de créer un dictionnaire dans lequel chaque clé correspond à un noeud du graphe et chaque valeur associée est une liste avec toutes les arêtes vers lequel va ce noeud. La fonction dijkstra parcours le graphe que ce dictionnaire modélise et détermine le plus cours chemin entre le point start et tous les points de la matrice, elle renvoie le temps en seconde du trajet le plus cours, ainsi que la succession de noeud pour y arriver. (C'est donc 2 output, un avec la matrice et tous les éléments, un vecteur avec le temps et le trajet)<br>
create_adjacency_dictionnary prend en paramètre la matrice d'accesibilité décrite précédemment et le point d'arrivé. La matrice d'accesibilité permet de créer le dictionnaire, et la position du end permet d'ajouter un point fictif (-1, -1, -1) qui indique à l'algorithme dijkstra quel est le point qui nous intéresse. dijkstra prend en paramètre un point de départ ainsi qu'un dictionnaire avec tous les noeuds et les arêtes qui en partent.

- Les fonctions get_path_to et get_path_textual permettent de retracer le chemin le plus cours entre le start et l'end trouvé par dijkstra. get_path_to renvoie les indexs des noeuds par lesquels passe le plus court chemin, get_path_textual permet de déterminer le chemin au format demandé.<br>
get_path_to prend en paramètre le noeud d'arrivé, la liste des noeuds précédents (fourni par dijkstra) ainsi que le dictionnaire des noeuds (fourni par create_adjacency_dictionnary)<br>
get_path_textual prend en paramètre la succession des indices des noeuds par lequel le plus court chemin passe (fourni par get_path_to)<br>
La fonction get_time_iter permet de chronométrer le temps d'execution du code et de récupérer les chemins associés à chacune des matrices, et la fonction draw_boxplot permet d'afficher les boxplots de N en fonction du temps d'exécution.<br>
get_time_iter prend en paramètre grilles (l'ensemble des matrices et point de départ/arrivé) et obstacles (qui permet, comme précédemment, de distinguer le cas du test sur la taille de la matrice du cas du test sur le nombre d'obstacles.)<br>
draw_boxplot prend en paramètre un DataFrame de deux colonnes (N et time) ainsi qu'obstacles (qui permet, comme précédemment, de distinguer le cas du test sur la taille de la matrice du cas du test sur le nombre d'obstacles.)

- La fonction create_output_file permet de créer le fichier de sorti au format demandé<br>
create_output_file prend en paramètre le nom du fichier de sorti ainsi que la liste des résultats (fourni par get_time_iter)

## PL.py
- la fonction create_model permet de résoudre le programme linéraire donné via gurobi<br>
create_model prend en paramètres m, n et p, ils permettent de déterminer le nombre de lignes, colonnes et d'obstacles
- fonction gen_matrix génère la matrice de 0 et de 1 en fonction du résultat donné par la résolution du programme linéaire<br>
gen_matrix prend les mêmes paramètres que create_model