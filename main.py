import utils
import PL
import sys
import traceback
import numpy as np

class BadArgument(Exception):
    pass

if __name__=="__main__":
    print(sys.argv)
    try:
        if sys.argv[1]=="-h":
            print("main.py m n p\n" \
            "m  (int) : nombre de lignes\n" \
            "n  (int) : nombre de colonnes\n" \
            "p  (int) : nombre d'obstacles\n")
        
        elif len(sys.argv)==4:
            m,n,p=sys.argv[1:]
            m,n,p=int(m),int(n),int(p)
            
            matrices=np.array(PL.gen_matrix(m,n,p))
            print(f"\nModèle valide : {len(matrices)} solution(s) optimale(s) trouvée(s) avec les paramètres ({n},{m},{p})")
            dx,dy,o="","",""
           
            while True:
                try:
                    dx,dy,o,fx,fy=input("Rentrer les coordonnées et l'orientation des points de départ et d'arrivé sous la forme dx dy o fx fy:\n").split(" ")
                except ValueError:
                    print("Mauvais arguments\nExemple: 10 3 sud 4 5")
                    continue
                
                if not(dx.isnumeric() and dy.isnumeric() and fx.isnumeric() and fy.isnumeric()):
                    print("dx,dy,fx et fy doivent être des entiers")
                    continue
                
                dx,dy,fx,fy=int(dx),int(dy),int(fx),int(fy)
                
                if not(0<=dx<=m and 0<=dy<=n and 0<=fx<=m and 0<=fy<=n):
                    print("dx et fx doivent appartenir à l'intervalle [0,m] (resp. [0,n] pour dy et fy)")
                    continue
                
                orientations=["n","o","s","e"]
                if o[0].lower() not in orientations:
                    print("o doit être une chaîne de caractère (nord,sud,est,ouest,n,s,e,o)")
                    continue
                o=orientations.index(o[0].lower())
                
                start_node,end_node=(dx,dy,o),(fx,fy)
                
                try:
                    possible_solutions=[]
                    for i in range(len(matrices)):
                        matrix=np.array(matrices[i])
                        #print(mogpl_functions.create_accessibility_matrix(matrix))
                        if utils.is_accessible(dx, dy, matrix) and utils.is_accessible(fx, fy, matrix):
                            possible_solutions.append(i)
                        elif i==len(matrices)-1:
                            raise Exception("Un des points de début ou de fin n'est pas accessible dans aucune des {len(matrices)} solutions.\n" \
                                            "Essayer avec d'autres points")
                except Exception as e:
                    print(e)
                    continue
                
                break
            
            solutions=[]
            for i in possible_solutions:
                print(f"Calcul de la solution n°{i}")
                matrix=matrices[i]
                try:
                    Mres=utils.create_accessibility_matrix(matrix)
                    dico=utils.create_adjacency_dictionnary(Mres,end_node)
                    _,pred=utils.dijkstra(start_node,dico)
                    solutions.append((i,utils.get_path_textual(utils.get_path_to((-1,-1,-1),pred,dico))))
                except utils.NoPathFoundError:
                    print("Pas de chemin pour la solution n°{i} du modèle")
                    pass
            print(f"{len(solutions)} soulution(s) retenue(s) pour les points {start_node} et {end_node}")
            for res in solutions:
                print(f"Solution optimale n°{res[0]} du modèle ({m},{n},{p}) : {res[1]}")
        else:
            raise BadArgument("Mauvais arguments. Essayez -h pour voir la syntaxe")
    except Exception:
        print(traceback.format_exc())
        