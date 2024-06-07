import argparse
import numpy as np
from Models.Traditional import  TraditionalModel
from Models.Permutation import  PermutationModel
from Models.Matching import  MatchingModel

from Utils.util import get_random_costs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modelo para resolver el problema SRR (Single Round Robin)")
    parser.add_argument("nteams", type=int, nargs="?", default=8, help="Número de equipos")
    parser.add_argument("--variant", type=str, default="permutation",
                        choices=["traditional", "matching", "permutation"], help="Variante del problema a resolver")
    parser.add_argument("--seed", type=int, default=42, help="Semilla para la generación de números aleatorios")
    parser.add_argument("--ratio", type=float, default=1, help="Proporción de costos aleatorios")

    args = parser.parse_args()

    for arg, val in args.__dict__.items():
        print(f"{arg}: {val}")

    assert args.nteams > 0, "La Cantidad de equipos debe ser Positivo."
    assert args.nteams % 2 == 0, "La cantidad de equipos debe ser par."

    models = {
        "traditional" : TraditionalModel,
        "matching": MatchingModel,
        "permutation": PermutationModel
    }

    assert args.variant in models.keys(), f"variante: {args.variant}."
    assert 0 <= args.ratio <= 1, f"Proporcion de costos fuera de rango."
    nteams = args.nteams

    costs = get_random_costs(args.nteams, args.ratio, args.seed)

    if nteams <= 6:
        # Integer small enough to see things.
        ones = np.where(costs)
        print(ones)
        print(list(zip(*ones)))

    model = models[args.variant](nteams, costs)

    model.optimize()

    for (i, pi), var in model.vars.items():
        print(f"Variable z[{i},{pi}]: {var.x}")