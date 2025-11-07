import numpy as np
tab=[0,1]
#print([(f"{x},{y},{z}",x-y+z) for x in tab for y in tab for z in tab])

M=np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])
#M=np.array([[0,0,0],[0,1,0],[0,0,1],[0,0,1]])
print(M)

def is_accessible(m,n,M):
    nb_lignes,nb_cols=M.shape
    print(M[max(0,m-1):min(m,nb_lignes-1)+1,max(0,n-1):min(n,nb_cols-1)+1])

is_accessible(3,0,M)
"""
Mres=np.zeros((M.shape[0]+1,M.shape[1]+1))
for m in range(M.shape[0]):
    for n in range(M.shape[1]):
        Mres[m,n]=is_accessible(m,n,M)

print(Mres)
"""