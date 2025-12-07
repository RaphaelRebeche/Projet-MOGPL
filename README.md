# Projet-MOGPL

## Introduction
Le rendu comporte trois fichiers python distinct.
- <code>main.py</code> comporte le programme nécessaire à la mise en place d'une interface demandé en question (e).
- <code>utils.py</code> comporte toutes les fonctions nécessaires à la réponse aux questions (a) à (d).
- <code>PL.py</code> comporte les fonctions nécessaires à la résolution du PL de la question (e).

Ainsi que les répertoires <code>tests</code> et <code>tests_rendu</code> qui comportent les fichiers d'entrée et de sortie des tests (et les images du rendu pour le second répertoire). Ainsi que le fichier <code>input_file.txt</code> qui est le fichier qui comporte la matrice d'exemple de l'énoncé.

### Bibliothèques externes
Pour notre projet nous utilisons certaines bibliothèques non natives à python:
- <code>gurobipy</code> pour faire appel à l'API de Gurobi.
- <code>numpy</code> pour faciliter la création et les calculs sur des matrices.
- <code>pandas</code> et <code>plotly</code> pour le calcul et l'affichage de graphiques sur la performance du programme.

## main.py
- Se lance en exécutant dans un terminal <code>python(3) {path}/main.py m n p</code><br>
Où <code>m</code>,<code>n</code> et <code>p</code> sont des entiers représentant le nombre de lignes, de colonnes et d'obstacles. Si le modèle est validé par le solveur, il vous sera demandé de rentrer 5 autres arguments <code>dx</code>, <code>dy</code>, <code>o</code>, <code>fx</code> et <code>fy</code>, séparés eux aussi par des espaces, où <code>dx</code>, <code>dy</code>, <code>fx</code> et <code>fy</code> sont des entiers représentant les lignes et les colonnes des poits de début et de fin et <code>o</code> une chaîne de caracère représentant un point cardinal (nord, ouest, sud, est, n, o, s, e).<br>
Si au moins un des deux points n'est pas accessibles dans aucunes des solutions renvoyées par le solveur il est demandé de réessayer avec d'autres coordonnées (dans certains cas, trouver deux points accessibles peut s'avérer fastidieux).<br>
Quand les points seronts validés, le script affichera dans le terminal la progression des calculs des chemins puis toutes les solutions trouvées.
- Ou en entrant le paramètre <code>-t input_path output_path</code> pour écrire la réponse des matrices du fichier <code>input_path</code> dans <code>output_path</code>.

## utils.py
- Les fonctions <code>is_accessible</code> et <code>create_accessibility_matrix</code> permettent de déterminer, à partir d'une matrice d'obstable, si un point est accessible et d'en déduire la matrice d'accessibilité.

- La fonction <code>create_random_matrix_start_end</code> permet de créer : une matrice comportant des 0 et des 1 qui modélisent l'absence où la présence d'un obstacle, un point start (ligne, colonne et orientation), un point end (ligne colonne). Chacune de ces matrices ou vecteurs est généré aléatoirement. 

- Les fonctions <code>append_matrix_to_file</code> et <code>create_file_test</code> permettent de créer un fichier au format de l'énoncé.

- La fonction <code>read_matrix</code> permet la lecture d'un fichier au format de l'énoncé en d'en extraire une liste où chaque ligne correspond à une matrice, le point de départ à d'arrivé qui lui sont associées.

- La fonction <code>create_adjacency_dictionnary</code> permet de créer un dictionnaire dans lequel chaque clé correspond à un noeud du graphe et chaque valeur associée est une liste avec toutes les arêtes vers lequel va ce noeud.

- La fonction <code>dijkstra</code> parcours le graphe modélisé par le dictionnaire d'adjacence et détermine le plus cours chemin entre le point start et tous les autres points de la matrice. Elle renvoie deux listes: le temps en seconde du trajet le plus cours, ainsi que la succession de noeud pour y arriver.

- Les fonctions <code>get_path_to</code> et <code>get_path_textual</code> permettent de retracer le chemin le plus cours entre le start et l'end trouvé par dijkstra. <code>get_path_to</code> renvoie les noeuds par lesquels passe le plus court chemin, <code>get_path_textual</code> permet de retourner le chemin au format demandé.

- La fonction <code>get_time_iter</code> permet de chronométrer le temps d'exécution du code et de récupérer les chemins associés à chacune des matrices, et la fonction draw_boxplot permet d'afficher les boxplots de N en fonction du temps d'exécution.

- La fonction <code>create_output_file</code> permet de créer le fichier de sortie au format demandé.

## PL.py
- la fonction <code>create_model</code> renvoie le modèle résolvant le programme linéaire demandé:

$$
\min z = \sum_{i=1}^{M} \sum_{j=1}^{N} a_{i,j} p_{i,j}
$$
$$
\left\{
\begin{array}{l}
\sum_{i=1}^{M} \sum_{j=1}^{N} a_{i,j} = P, \\
\sum_{j=1}^{M} a_{i,j} \leq \frac{2P}{M} \quad \forall i \in [1, M], \\
\sum_{j=1}^{N} a_{i,j} \leq \frac{2P}{N} \quad \forall j \in [1, N], \\
a_{i,j} - a_{i,j+1} + a_{i,j+2} < 2 \quad \forall i \in [1, M], \, j \in [1, N-2], \\
a_{i,j} - a_{i+1,j} + a_{i+2,j} < 2 \quad \forall i \in [1, M-2], \, j \in [1, N]
\end{array}
\right.
$$

- la fonction <code>gen_matrices</code> génère les matrices de 0 et de 1 en fonction des réponses données par le solveur.