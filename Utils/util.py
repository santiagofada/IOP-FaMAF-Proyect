import numpy as np
import  argparse

def sort_match(i, j):
    """
    Los partidos podrian no estar ordenados, pero sera mas comodo trabajar con tuplas ordenas.
    El orden viene dado por el primer equipo, es decir que esta funcion lleva un partido (j,i) a (i,j) si i<j
    """
    if i < j:
        return (i, j)
    else:
        assert j < i, "Un equipo no puede jugar contra si mismo."
        return (j, i)

def get_random_costs(nteams, ratio, seed) -> np.array:
    np.random.seed(seed)

    n_rounds = nteams - 1 # Cantidad de fechas
    n_matches = ((nteams * (nteams - 1)) // 2) # Cantidad de equipos
    n_elements_costs = n_matches * n_rounds # Cantidad de variables de decision
    n_selected = int(n_elements_costs * ratio)  # Proporcion de variables de decision con costo no nulo

    costs = np.zeros((nteams, nteams, n_rounds), dtype=int)
    choices_matches = np.random.choice(np.arange(n_elements_costs), size=n_selected, replace=False) # Tomar solo n_selected variables de decision de la matriz original

    # Tomamar los elementos a los que les vamos a asignar costo 1
    lower_i, lower_j = np.where(np.arange(nteams)[:, np.newaxis] < np.arange(nteams)[np.newaxis, :])
    # asignar el costo
    costs[lower_i[choices_matches % n_matches], lower_j[choices_matches % n_matches], choices_matches // n_matches] = 1
    # La matriz debe ser simetrica
    costs[lower_j[choices_matches % n_matches], lower_i[choices_matches % n_matches], choices_matches // n_matches] = 1
    assert costs.sum() == n_selected * 2
    return costs

def read_config_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    nteams = int(lines[0].strip())
    data = []

    for line in lines[1:]:
        if line.strip():
            parts = line.split(',')

            i = parts[0].strip().strip('(').split()
            j = parts[1].strip().strip(')').split()
            i, j = int(i[0]), int(j[0])
            round = int(parts[2].strip())

            cost = float(parts[3].strip())
            data.append((i, j, round, cost))

    return nteams, data

def build_cost_matrix(nteams, data):
    costs = np.zeros((nteams, nteams, nteams - 1))
    for i, j, round, cost in data:
        costs[i, j, round] = cost
    return costs

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', 's', 'si'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
