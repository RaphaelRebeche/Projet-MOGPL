import gurobipy as gp
from gurobipy import GRB
import random

def create_model(n,m,p):
    """
    Renvoie le modèle gurobipy
    
    :param n: Nombre de lignes de la matrice
    :param m: Nombre de colonnes de la matrice
    :param p: Nombre d'obstacles de la matrice
    """
    model=gp.Model("opt")

    dico_var={}
    for i in range(n):
        for j in range(m):
            dico_var[f"a_{i}_{j}"]=model.addVar(vtype=GRB.BINARY, name=f"a_{i}_{j}")
            dico_var[f"p_{i}_{j}"]=random.randint(0,1000)
    
    #Définition de la fonction objectif
    model.setObjective(
        gp.quicksum(dico_var[f"p_{i}_{j}"]*dico_var[f"a_{i}_{j}"] for i in range(n) for j in range(m)),
        GRB.MINIMIZE       
            )
    
    #Définition des contraintes
    model.addConstr(
        gp.quicksum(dico_var[f"a_{i}_{j}"] for i in range(n) for j in range(m))==p,
        name="C_nb_obstacles"
    )
    
    for i in range(n):#Contraintes de ligne
        model.addConstr(
            gp.quicksum(dico_var[f"a_{i}_{j}"] for j in range(m))<=2*p/m,
            name=f"C_ligne_{i}"
        )
        
        for j in range(m-2):
            model.addConstr(
                dico_var[f"a_{i}_{j}"]-dico_var[f"a_{i}_{j+1}"]+dico_var[f"a_{i}_{j+2}"]<=1,#Strictement inférieur à 2 mais '<' non supporté
                name=f"C_101_{i}-{j}_{i}-{j+2}"
            )
    
    for j in range(m):#Contraintes de colonne
        model.addConstr(
            gp.quicksum(dico_var[f"a_{i}_{j}"] for i in range(n))<=2*p/n,
            name=f"C_colonne_{j}"
            )
        
        for i in range(n-2):
            model.addConstr(
                dico_var[f"a_{i}_{j}"]-dico_var[f"a_{i+1}_{j}"]+dico_var[f"a_{i+2}_{j}"]<=1,
                name=f"C_101_{i}-{j}_{i+2}-{j}"
            )

    model.optimize()
    return model

if __name__=="__main__":
    random.seed(7)
    model=create_model(50,50,50)
    
    if model.status == GRB.OPTIMAL:
        print(f"Optimal objective value: {model.objVal}")
    else:
        print("No optimal solution found.")   
    
    print(len(list(model.getConstrs())))
    for var in model.getVars():
        pass
        #print(var.varName,var.X)
    model.write("myfile.lp")