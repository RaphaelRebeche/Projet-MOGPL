import gurobipy as gp
from gurobipy import GRB
import random
import numpy as np

def create_model(m,n,p):
    """
    Renvoie le modèle gurobipy
    
    :param m: Nombre de lignes de la matrice
    :param m: Nombre de colonnes de la matrice
    :param p: Nombre d'obstacles de la matrice
    """
    model=gp.Model("opt")

    dico_var={}
    for i in range(m):
        for j in range(n):
            dico_var[f"a_{i}_{j}"]=model.addVar(vtype=GRB.BINARY, name=f"a_{i}_{j}")
            dico_var[f"p_{i}_{j}"]=random.randint(0,1000)# entier représentant le coût pour placer un bloc sur cette case
    
    #Définition de la fonction objectif
    model.setObjective(
        gp.quicksum(dico_var[f"p_{i}_{j}"]*dico_var[f"a_{i}_{j}"] for i in range(m) for j in range(n)),
        GRB.MINIMIZE       
            )
    
    #Définition des contraintes
    model.addConstr(
        gp.quicksum(dico_var[f"a_{i}_{j}"] for i in range(m) for j in range(n))==p,
        name="C_nb_obstacles"
    )
    
    for i in range(m):#Contraintes de ligne
        model.addConstr(
            gp.quicksum(dico_var[f"a_{i}_{j}"] for j in range(n))<=2*p/m,
            name=f"C_ligne_{i}"
        )
        
        for j in range(n-2):
            model.addConstr(
                dico_var[f"a_{i}_{j}"]-dico_var[f"a_{i}_{j+1}"]+dico_var[f"a_{i}_{j+2}"]<=1,#Strictement inférieur à 2 mais '<' non supporté
                name=f"C_101_{i}-{j}_{i}-{j+2}"
            )
    
    for j in range(n):#Contraintes de colonne
        model.addConstr(
            gp.quicksum(dico_var[f"a_{i}_{j}"] for i in range(m))<=2*p/n,
            name=f"C_colonne_{j}"
            )
        
        for i in range(m-2):
            model.addConstr(
                dico_var[f"a_{i}_{j}"]-dico_var[f"a_{i+1}_{j}"]+dico_var[f"a_{i+2}_{j}"]<=1,
                name=f"C_101_{i}-{j}_{i+2}-{j}"
            )

    model.optimize()
    return model

def gen_matrix(m,n,p):
    model=create_model(m,n,p)
    if model.Status==GRB.OPTIMAL:
        res=[]
        for k in range(model.SolCount):
            model.Params.SolutionNumber=k#Solution k du problème
            res.append([[int(model.getVarByName(f"a_{i}_{j}").Xn) for j in range(n)] for i in range(m)])
        return res
    raise Exception("Modèle irréalisable!")

if __name__=="__main__":
    pass