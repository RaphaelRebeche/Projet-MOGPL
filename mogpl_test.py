import numpy as np

# lecture fichier d'entrée
def read_matrix(file="input_file.txt"):
    with open(file, "r") as f:
        file = f.readlines()

        for i, line in enumerate(file):
            if i == 0:
                line = line.split(" ")
                line = list(map(int, line))
                m, n = int(line[0]), int(line[1])
                matrix = np.zeros(shape=(m, n))

            elif i <= m:
                line = line.split(" ")
                line = list(map(int, line))
                matrix[i - 1] = line

            elif i == m + 1:
                line = [val.strip() for val in line.split(" ")]
                start = [line[0], line[1]]
                stop = [line[2], line[3]]
                if line[4] == "nord":
                    start.append(0)
                elif line[4] == "ouest":
                    start.append(1)
                elif line[4] == "sud":
                    start.append(2)
                elif line[4] == "est":
                    start.append(3)
                else:
                    print("erreur de direction")
                start = list(map(int, start))
                stop = list(map(int, stop))
            else:
                pass
    return np.array(matrix, dtype=int), start, stop


# ================ Main ====================
matrix, start, stop = read_matrix()
print(matrix, start, stop)

M=np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])
M=np.array([[0,0,0],[0,1,0],[0,0,1],[0,0,1]])
print(M)

def is_accessible(i,j,M):
    return not M[max(0,i-1):min(i,M.shape[0]-1)+1,max(0,j-1):min(j,M.shape[1]-1)+1].sum()

def create_accessibility_matrix(M):
    return np.array([[is_accessible(i,j,M) for j in range(M.shape[1]+1)]for i in range(M.shape[0]+1)],dtype=int)

def create_adjacency_dictionnary(accessibility_matrix):
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

    return dico_node

Mres=create_accessibility_matrix(M)
dico=create_adjacency_dictionnary(Mres)

#print(dico.keys())
for i in range(4):
    print(dico[(3,0,i)])
