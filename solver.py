import argparse
from Utils.util import str2bool
from Utils.util import read_config_file
from Utils.util import  build_cost_matrix

from Models.Traditional import TraditionalModel
from Models.Permutation import PermutationModel
from Models.Matching import MatchingModel




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modelo para resolver el problema SRR (Single Round Robin)")
    #parser.add_argument("--nteams", type=int, nargs="?", default=8, help="Número de equipos")
    parser.add_argument("--variant", type=str, default="traditional",
                        choices=["traditional", "matching", "permutation"], help="Variante del problema a resolver")

    parser.add_argument("--entera", type=str2bool, default=True, help="Indica si las variables deben ser binarias (enteras) en lugar de continuas")
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
        "matching": MatchingModel,
        "permutation": PermutationModel
    }

    assert args.variant in models.keys(), f"variante: {args.variant}."
    assert nteams > 0, "La Cantidad de equipos debe ser Positivo."
    assert nteams % 2 == 0, "La cantidad de equipos debe ser par."
    #assert 0 <= args.ratio <= 1, f"Proporcion de costos fuera de rango."

    """
    for k,v in models.items():


        model = models[k](nteams, costs, entera)

        model.optimize()
        print(f"RESPUESTA {k}")

        Var = model.get_nonzero_vars()
        for var in Var:
            print(var)
        print(f"valor de la funcion objetivo: {model.get_objval()}")
        print("\n")
    """
    model = models[args.variant](nteams, costs, entera)
    model.optimize()



    print(f"\n\nrespuesta formulacion {args.variant}")

    Var = model.get_nonzero_vars()
    for var in Var:
        print(var)
    print(f"valor de la funcion objetivo: {model.get_objval()}")
    print("\n")
