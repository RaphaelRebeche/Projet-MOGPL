import numpy as np
import time
import pandas as pd

class NoPathFoundError(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)

def is_accessible(i,j,M):#Renvoie Vrai si accessible, Faux sinon
    return not M[max(0,i-1):min(i,M.shape[0]-1)+1,max(0,j-1):min(j,M.shape[1]-1)+1].sum()

def create_accessibility_matrix(M):
    return np.array([[is_accessible(i,j,M) for j in range(M.shape[1]+1)]for i in range(M.shape[0]+1)],dtype=int)

def create_adjacency_dictionnary(accessibility_matrix,end_point):
    nblines,nbcols=accessibility_matrix.shape
    dico_node={}
    for node in list(np.argwhere(accessibility_matrix==1)):
        node=tuple(map(int,node))
        for i in range(4):
            dico_node[(node[0],node[1],i)]=[(node[0],node[1],(i-1)%4),(node[0],node[1],(i+1)%4)]
    
    for node in dico_node.keys():
        if node[2]==2 or node[2]==3:#On ne vérifie les chemins que lorsque l'on se délpace à l'Est ou au Sud, on en déduit les déplacements vers l'Ouest ou le Nord
            i,j=node[0],node[1]
            nb_possible_neighbours_i,nb_possible_neighbours_j=min(3,nblines-1-i),min(3,nbcols-1-j)
            if node[2]==2:
                for k in range(1,nb_possible_neighbours_i+1):
                    if accessibility_matrix[i+k,j]:
                        dico_node[(i,j,2)].append((i+k,j,2))
                        dico_node[(i+k,j,0)].append((i,j,0))
                    else:
                        break
            
            elif node[2]==3:
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
    #Algorithme pour ce cas spécifique où toutes les arêtes ont un poids fixé (ici 1)
    #Création d'un dictionnaire d'index
    node_list=list(dico_node.keys())
    dico_idx={val:node_list.index(val) for val in node_list}
    
    #Initialisation
    distances_to_node=np.array([np.inf for _ in range(len(node_list))])
    predecessor_list=np.array([-1 for _ in range(len(node_list))])
    distances_to_node[dico_idx[start_node]]=0
    predecessor_list[dico_idx[start_node]]=dico_idx[start_node]
    

    Q=node_list.copy()#Nœuds à visiter

    #Itération
    while len(Q)!=0:
        path_found=False

        #Trouver lle nœud le plus proche parmi tous ceux accessibles
        min_dist=np.inf
        for node in Q:
            if distances_to_node[dico_idx[node]]<min_dist:
                path_found=True#booléen pour vérifier si un nouveau chemin a été trouvé
                min_dist=distances_to_node[dico_idx[node]]
                curr_node=node
                curr_node_idx=dico_idx[curr_node]
                curr_node_dist=distances_to_node[dico_idx[curr_node]]
        
        if path_found:
            Q.remove(curr_node)
        
            for neigh_node in dico_node[curr_node]:
                if distances_to_node[dico_idx[neigh_node]]>curr_node_dist+1:#Tous les poids sont de 1 dans ce graphe
                    distances_to_node[dico_idx[neigh_node]]=curr_node_dist+1
                    predecessor_list[dico_idx[neigh_node]]=curr_node_idx
        
        else:#Plus de nœuds accessibles dans la composante connexe du nœud de départ, c'est un problème si on cherche le chemin entre
            print("\033[93mPlusieurs composantes connexes dans le graphe\033[0m")
            break
    
    return distances_to_node,predecessor_list

def get_path_to(end_node,predecessor_list,dico_node):
    node_list=list(dico_node.keys())
    end_node_idx=node_list.index(end_node)
    if predecessor_list[end_node_idx]==-1:
        raise NoPathFoundError(f"Pas de chemin existant vers le nœud recherché {end_node}")
    path=[predecessor_list[end_node_idx]]
    while path[-1]!=pred[path[-1]]:
        path.append(pred[path[-1]])
    path=path[::-1]

    res=[]
    for idx in path:
        res.append(node_list[idx])
    return res

def get_path_textual(path):
    curr_node=path[0]
    res=""
    nb_step=0
    for node in path[1:]:
        if curr_node[0]!=node[0] or curr_node[1]!=node[1]:
            res+=f"a{abs(curr_node[0]-node[0]+curr_node[1]-node[1])} "
        elif (curr_node[2]+1)%4==node[2]:
            res+="G "
        else:
            res+="D "
        curr_node=node
        nb_step+=1
    return str(nb_step)+" "+res[:-1]

def create_adjacency_matrix(adjacency_dictionnary):
    node_list=list(adjacency_dictionnary.keys())
    mat=np.zeros((len(node_list),len(node_list)))
    for in_node_idx in range(len(node_list)):
        for out_node in adjacency_dictionnary[node_list[in_node_idx]]:
            mat[in_node_idx,node_list.index(out_node)]+=1
    return mat
        

# lecture fichier d'entrée
def read_matrix(nom_fichier):
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
            
            if ligne[0]=='#':# Ignorer les commentaires
                continue
            # Lecture matrice
            largeur, hauteur = map(int, ligne.split())
            matrice = np.zeros(shape=(largeur, hauteur))
            for i in range(hauteur):
                ligne_vals = list(map(int, f.readline().split()))
                matrice[i] = ligne_vals

            # Lecture start end et orientation
            params = f.readline().split()
            li_start, col_start, li_end, col_end = map(int, params[:4])
            orientation = params[4]
            start, end = [li_start, col_start], [li_end, col_end]

            if orientation == "nord":
                start.append(0)
            elif orientation == "ouest":
                start.append(1)
            elif orientation == "sud":
                start.append(2)
            elif orientation == "est":
                start.append(3)
            else:
                print(
                    f"erreur direction : {orientation} \n, start : {start}, end : {end}"
                )

            # ligne séparatrice (0 0)
            f.readline()

            grilles.append((matrice, start, end))

    return grilles 

# ================ Main ====================
if __name__=="__main__":
    """
    start_time=time.time()
    matrix, start, end = read_matrix()
    start=tuple(start)
    #print(matrix, start, end)
    Mres=create_accessibility_matrix(matrix)
    #print(Mres)
    dico=create_adjacency_dictionnary(Mres,end)
    #adj_mat=create_adjacency_matrix(dico)
    #print(list(dico.keys())[:3],list(dico.keys())[-3:])
    #print()
    #print(adj_mat)
    d,pred=dijkstra(start,dico)
    print(d)
    #d[-1]=distance+1 (poids des arêtes vers le nœud fictif=1)
    #print(Mres.sum()*4+1)
    #print(d,len(d))
    print(list(dico.keys()).index(start))
    print(start)
    path=get_path_to((-1,-1,-1),pred,dico)
    print(get_path_textual(path))
    #print(get_path_textual(get_path_to((0,0,0))))
    end_time=time.time()
    print(f"{end_time-start_time}s")
    """

    grilles = read_matrix("input_file_test_obstacle.txt")
    time_iter = pd.DataFrame(columns=["size", "time"])
    
    error_list=[]
    for i in range(len(grilles)):
        size = len(grilles[i][0])
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
            d, pred = dijkstra(start, dico)
            path = get_path_to((-1, -1, -1), pred, dico)  # Nœud fictif représentant le point final
            print(get_path_textual(path))
        except NoPathFoundError:
            error_list.append((Mres,start,end))

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        time_iter = pd.concat(
            [time_iter, pd.DataFrame([[size, execution_time]], columns=time_iter.columns)],
            ignore_index=True,
        )
        print(f"{time_iter}") 
    print(len(error_list))