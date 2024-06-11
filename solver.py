import argparse
import numpy as np
from Models.Traditional import TraditionalModel
from Models.Permutation import PermutationModel
from Models.Matching import MatchingModelaux


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modelo para resolver el problema SRR (Single Round Robin)")
    #parser.add_argument("--nteams", type=int, nargs="?", default=8, help="Número de equipos")
    parser.add_argument("--variant", type=str, default="traditional",
                        choices=["traditional", "matching", "permutation"], help="Variante del problema a resolver")

    parser.add_argument("--entera", type=bool, default=True, help="Indica si las variables deben ser binarias (enteras) en lugar de continuas")
    parser.add_argument("--file", type=str, required=True, help="Archivo de configuración")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para la generación de números aleatorios")
    # parser.add_argument("--ratio", type=float, default=1, help="Proporción de costos aleatorios")

    args = parser.parse_args()

    #for arg, val in args.__dict__.items():
    #    print(f"{arg}: {val}")


    config_file_path = args.file

    nteams, data = read_config_file(config_file_path)
    costs = build_cost_matrix(nteams, data)
    entera = args.entera

    models = {
        "traditional" : TraditionalModel,
        "matching": MatchingModelaux,#MatchingModel,#
        "permutation": PermutationModel
    }

    assert args.variant in models.keys(), f"variante: {args.variant}."
    assert nteams > 0, "La Cantidad de equipos debe ser Positivo."
    assert nteams % 2 == 0, "La cantidad de equipos debe ser par."
    #assert 0 <= args.ratio <= 1, f"Proporcion de costos fuera de rango."


    for k,v in models.items():

        #model = models[args.variant](nteams, costs, entera)

        model = models[k](nteams, costs, entera)

        model.optimize()
        print(f"RESPUESTA {k}")
        #(f"RESPUESTA {args.variant}")

        Var = model.get_nonzero_vars()
        for var in Var:
            print(var)
        print(f"valor de la funcion objetivo: {model.get_objval()}")
        print("\n")