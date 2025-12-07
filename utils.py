import numpy as np
import pandas as pd
import time
import os
import plotly.express as px

class NoPathFoundError(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)

def is_accessible(i,j,M):
    """
    Vérifie si le robot peut marcher sur l'intersection (i,j)
    
    Args:
        i (int): Ligne de l'intersection
        j (int): Colonne de l'intersection
        M (numpy.ndarray): Matrice d'entrée

    Returns:
        bool: Vrai si le robot peut marcher sur cette intersection
    """
    return not M[max(0,i-1):min(i,M.shape[0]-1)+1,max(0,j-1):min(j,M.shape[1]-1)+1].sum()

def create_accessibility_matrix(M):
    """
    Renvoie la matrice d'accessibilité : la matrice des intersections où le robot peur marcher
    
    Args:
        M (numpy.ndarray): Matrice d'entrée

    Returns:
        numpy.ndarray: Où les 1 représentent là où le robot peut marcher
    """
    return np.array([[is_accessible(i,j,M) for j in range(M.shape[1]+1)]for i in range(M.shape[0]+1)],dtype=int)

def create_adjacency_dictionnary(accessibility_matrix,end_point):
    """
    Renvoie un dictionnaire des adjacences
    
    Args:
        Maccessibility_matrix (numpy.ndarray): Matrice d'entrée
        end_point (tuple): coordonnées du point d'arrivée

    Returns:
        dict: dictionnaire de la forme {(i,j,o) : [(i',j',o')*]})
    """
    nblines,nbcols=accessibility_matrix.shape
    dico_node={}
    for node in list(np.argwhere(accessibility_matrix==1)):
        node=tuple(map(int,node))
        for i in range(4):#Pour tous les nœuds, il est possible de tourner à gauche au à droite
            dico_node[(node[0],node[1],i)]=[(node[0],node[1],(i-1)%4),(node[0],node[1],(i+1)%4)]
    
    for node in dico_node.keys():
        if node[2]==2 or node[2]==3:#On ne vérifie les chemins que lorsque l'on se délpace à l'est ou au sud, on en déduit les déplacements vers l'ouest et le nord
            i,j=node[0],node[1]
            nb_possible_neighbours_i,nb_possible_neighbours_j=min(3,nblines-1-i),min(3,nbcols-1-j)
            
            if node[2]==2:#On regarde si on peut aller vers le sud
                for k in range(1,nb_possible_neighbours_i+1):
                    if accessibility_matrix[i+k,j]:
                        dico_node[(i,j,2)].append((i+k,j,2))
                        dico_node[(i+k,j,0)].append((i,j,0))
                    else:
                        break
            
            elif node[2]==3:#On regarde si on peut aller vers l'est
                for k in range(1,nb_possible_neighbours_j+1):
                    if accessibility_matrix[i,j+k]:
                        dico_node[(i,j,3)].append((i,j+k,3))
                        dico_node[(i,j+k,1)].append((i,j,1))
                    else:
                        break

    #Création des liens vers le point fictif de fin : (-1,-1,-1)
    dico_node[(-1,-1,-1)]=[]
    for i in range(4):
        dico_node[(end_point[0],end_point[1],i)].append((-1,-1,-1))

    return dico_node

def dijkstra(start_node,dico_node):
    """
    Calcul des distances entre un point et tous ceux qui lui sont accessible
    
    Args:
        start_node (tuple): coordonnées du point de début
        dico_node (dict): dictionnaire de la forme {(i,j,o) : [(i',j',o')*]})

    Returns:
        distances_to_node (list): distances par rapport au point de départ
        predecessor_list (list): liste d'entiers qui à l'index i a pour valeur l'index i' du nœud qui le précède
            Si predecessor_list[i]==i, cela veut dire que i est le point de départ
    """
    #Algorithme pour ce cas spécifique où toutes les arêtes ont un poids fixé (ici 1)
    #Création d'un dictionnaire d'index
    node_list=list(dico_node.keys())
    dico_idx={val:node_list.index(val) for val in node_list}
    
    #Initialisation
    distances_to_node=np.full(len(node_list),np.inf)
    predecessor_list=np.full(len(node_list),-1)
    distances_to_node[dico_idx[start_node]]=0
    predecessor_list[dico_idx[start_node]]=dico_idx[start_node]
    
    visited_nodes=np.zeros(len(node_list),dtype=bool)

    #Itérations
    while True:

        #Trouver le nœud le plus proche parmi tous ceux accessibles
        min_dist=np.inf
        curr_node_idx=-1

        for idx in range(len(distances_to_node)):
            if not visited_nodes[idx] and distances_to_node[idx]<min_dist:
                min_dist=distances_to_node[idx]
                curr_node_idx=idx
        
        if curr_node_idx==-1:#Si plusieurs composantes connexes ou graphe complètement visité
            break
        
        visited_nodes[curr_node_idx]=True
        curr_node=node_list[curr_node_idx]
        curr_node_dist=distances_to_node[curr_node_idx]

        for neigh_node in dico_node[curr_node]:
            neigh_node_idx=dico_idx[neigh_node]
            new_dist=curr_node_dist+(neigh_node!=(-1,-1,-1))#poids de 1 si arête normale, poids de 0 si arête fictive

            if new_dist<distances_to_node[neigh_node_idx]:#Tous les poids sont de 1 dans ce graphe
                distances_to_node[neigh_node_idx]=new_dist
                predecessor_list[neigh_node_idx]=curr_node_idx
    
    return distances_to_node,predecessor_list

def get_path_to(end_node,predecessor_list,dico_node):
    """
    Renvoie le chemin entre deux nœuds A et B
    
    Args:
        end_node (tuple): coordonnées du point de début
        predecessor_list (list): liste des prédecessurs retournée par dijkstra
        dico_node (dict): dictionnaire de la forme {(i,j,o) : [(i',j',o')*]})

    Returns:
        path: liste des nœuds entre A et B
    """
    node_list=list(dico_node.keys())
    end_node_idx=node_list.index(end_node)
    if predecessor_list[end_node_idx]==-1:
        raise NoPathFoundError(f"Pas de chemin existant vers le nœud recherché : {end_node}")
    
    path=[end_node_idx]
    while path[-1]!=predecessor_list[path[-1]]:
        path.append(predecessor_list[path[-1]])
    path=path[::-1]

    res=[]
    for idx in path:
        res.append(node_list[idx])
    
    if res[-1]==(-1,-1,-1):#Si le dernier nœoud est le point fictif, on ne le renvoie pas
        res=res[:-1]
    return res

def get_path_textual(path):
    """
    Renvoie le chemin entre deux nœuds
    
    Args:
        path (list): liste des nœuds sur le chemin

    Returns:
        res (str): Chemin sous la forme demandée
    """
    curr_node=path[0]
    res=str(len(path)-1)
    for next_node in path[1:]:
        if curr_node[0]!=next_node[0] or curr_node[1]!=next_node[1]:#Si la position en x ou en y change alors on avance
            res+=f" a{abs(curr_node[0]-next_node[0]+curr_node[1]-next_node[1])}"
        elif (curr_node[2]+1)%4==next_node[2]:
            res+=" G"
        else:
            res+=" D"
        curr_node=next_node
    return res

#Lecture de fichiers d'entée
def read_matrix(nom_fichier):
    """
    Renvoie une liste de toutes les grilles, points de début et d'arrivée d'un fichier
    
    Args:
        nom_fichier (str): chemin vers le fichier

    Returns:
        grilles (list): liste des grilles sous la forme[(numpy.ndarray,tuple,tuple)*]
    """
    grilles = []

    with open(nom_fichier, "r") as f:
        while True:
            ligne = f.readline()
            # On assure la fin de la boucle à la fin du fichier
            if not ligne:
                break

            # On s'assure de passer une ligne si elle est vide (normalement inutile)
            ligne = ligne.strip()
            if not ligne:
                continue

            # On passe les commentaires
            if ligne[0] == "#":
                continue

            # Lecture matrice
            n_lignes, n_colonnes = map(int, ligne.split())
            matrice = np.zeros(shape=(n_lignes, n_colonnes))
            for i in range(n_lignes):
                ligne_vals = list(map(int, f.readline().split()))
                matrice[i] = ligne_vals

            # Lecture start end et orientation
            params = f.readline().split()
            li_start, col_start, li_end, col_end = map(int, params[:4])
            orientation = params[4]

            try:
                o=["n","o","s","e"].index(orientation[0].lower())
            except:
                raise Exception(f"erreur de direction : {orientation}")

            start, end = (li_start, col_start,o), (li_end, col_end)
            # ligne séparatrice (0 0)
            f.readline()
            grilles.append((matrice, start, end))

    return grilles

def get_time_iter(grilles, obstacles=False):
    """
    Renvoie une matrice du temps d'exécution en fonction de la grille d'entrée et une liste des plus courts chemin
    
    Args:
        grilles (list): liste des grilles sous la forme[(numpy.ndarray,tuple,tuple)*]
        obstacles (bool): indique si les grilles d'entrée permettent de tester la taille ou le nombre d'obstacles

    Returns:
        time_iter (DataFrame): deux colonnes "N" et "time"
        chemin (list): list de str
    """
    chemin = []

    time_iter = pd.DataFrame(columns=["N", "time"])

    for i in range(len(grilles)):
        if(i%10==0):
            print(f"Test n°{i}")

        if not obstacles:
            size = len(grilles[i][0])
        else:
            size = np.sum(grilles[i][0])
        start_time, end_time = 0, 0
        start_time = time.perf_counter()

        matrix, start, end = (
            grilles[i][0],  # matrix
            grilles[i][1],  # start
            grilles[i][2],  # end
        )
        start = tuple(start)

        Mres = create_accessibility_matrix(matrix)
        dico = create_adjacency_dictionnary(Mres, end)

        try:
            _, pred = dijkstra(start, dico)
            path = get_path_to(
                (-1, -1, -1), pred, dico
            )  # Nœud fictif représentant le point final
            chemin.append(f"{get_path_textual(path)} ")

        except NoPathFoundError:
            chemin.append("-1")
            continue

        _, pred = dijkstra(start, dico)
        path = get_path_to(
            (-1, -1, -1), pred, dico
        )  # as (-1, -1, -1) is our fictif point
        # print(path)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        time_iter.loc[len(time_iter)]=[size,execution_time]
    return time_iter, chemin


def draw_boxplot(time_iter, obstacle=False):
    """
    Affiche les boxplots correspondant à chacune des valeurs de N dans le DataFrame d'entrée
    
    Args:
        time_iter (DataFrame): deux colonnes "N" et "time"
        obstacles (bool): indique si les grilles d'entrée permettent de tester la taille ou le nombre d'obstacles
    """
    if obstacle:
        fig = px.box(
            time_iter,
            x="N",
            y="time",
            title="Temps d'execution en fonction du nombre d'obstacles",
        )
    else:
        fig = px.box(
            time_iter,
            x="N",
            y="time",
            title="Temps d'execution en fonction de la taille de la grille",
        )
    fig.show()

    
def create_output_file(file_path, chemin):
    """
    Créer un fichier avec tous les plus cours chemins
    
    Args:
        nom_fichier (str): chemin vers le fichier
        chemin (list): list de str
    """
    file = os.path.basename(file_path)
    with open(file, "w") as f:
        for row in chemin:
            f.write(f"{row} \n")

# ================ Main ====================
if __name__=="__main__":
    
    matrix,start_node,end_node=read_matrix("input_file.txt")[0]
    Mres=create_accessibility_matrix(matrix)
    dico=create_adjacency_dictionnary(Mres,end_node)
    d,pred=dijkstra(start_node,dico)
    path=get_path_to((-1,-1,-1),pred,dico)
    print(get_path_textual(path))

    grilles_obstacles=read_matrix("input_file_test_obstacle.txt")
    time_iter_obstacle,chemin_obstacle=get_time_iter(grilles_obstacles,obstacles=True)
    create_output_file("output_file_test_obstacle.txt",chemin_obstacle)

    grilles_size=read_matrix("input_file_test_size.txt")
    time_iter_size,chemin_size=get_time_iter(grilles_size,obstacles=False)
    create_output_file("output_file_test_size.txt",chemin_size)
