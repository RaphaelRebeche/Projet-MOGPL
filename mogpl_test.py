import numpy as np

tab = [0, 1]
# print([(f"{x},{y},{z}",x-y+z) for x in tab for y in tab for z in tab])

M = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
M = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1]])
# print(M)


def is_accessible(m, n, M):
    nb_lignes, nb_cols = M.shape
    return (
        M[
            max(0, m - 1) : min(m, nb_lignes - 1) + 1,
            max(0, n - 1) : min(n, nb_cols - 1) + 1,
        ].sum()
        != 0
    )


is_accessible(3, 0, M)

Mres = np.zeros((M.shape[0] + 1, M.shape[1] + 1))
for m in range(Mres.shape[0]):
    for n in range(Mres.shape[1]):
        Mres[m, n] = is_accessible(m, n, M)

# print(Mres)


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
