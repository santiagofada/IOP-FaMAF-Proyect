import pyscipopt as ps
import itertools
import numpy as np
from Utils.util import sort_match


class TraditionalModel:
    def __init__(self, nteams, costs, entera=False, **kwargs) -> None:
        assert costs.shape == (nteams, nteams, nteams-1), "Incorrect dimensions"

        self.model : ps.Model = None
        self.nteams : int = nteams
        self.costs : np.array = costs

        self._build(entera=entera, **kwargs)

    def _build(self, entera=False, timelimit=None):
        assert self.model is None, "Modelo ya inicializado"

        self.model = ps.Model(f"Minimize carry-over effect for {self.nteams} teams", enablepricing=False)
        self.model.redirectOutput()
        self.model.setParam("display/freq", 1)

        teams = range(self.nteams)
        rounds = range(self.nteams - 1)
        matches = list(itertools.combinations(teams, r=2))

        # variables X, sera un conjunto
        if entera:
            # variables enteras
            x = {
                ((i,j),r):self.model.addVar(name=f"x[{i},{j},{r}]", lb=0.0, ub=1.0,
                                            vtype=("B"))
                for ((i,j),r) in itertools.product(matches, rounds)
            }
        else:
            # variables reales
            x = {
                ((i, j), r): self.model.addVar(name=f"x[{i},{j},{r}]", lb=0.0, ub=1.0,
                                               vtype=("C"))
                for (i, j), r in itertools.product(matches, rounds)
            }

        # Funcion objetivo c_{m,r} * x_{m,r}
        self.model.setObjective(
            ps.quicksum(
                cost * x[(i, j), r]
                for (i, j, r), cost in np.ndenumerate(self.costs)
                if np.abs(cost) > 1e-6 and i < j
            ),
            sense="minimize"
        )

        # Restricciones

        # T2. Un partido se juega una unica vez
        for (i, j) in matches:
            self.model.addCons(
                ps.quicksum(x[(i, j), r] for r in rounds) == 1
            )

        # T3.  un partido solo se puede jugar una unica vez por ronda
        for i, r in itertools.product(teams, rounds):
            self.model.addCons(
                ps.quicksum(x[sort_match(i, j), r] for j in teams if i != j) == 1
            )

        # Time limit if it's integral.
        if entera and timelimit is not None:
            self.model.setParam('limits/time', timelimit)

    def optimize(self):
        self.model.optimize()
        #self.model.printStatistics()

    def get_objval(self):
        # Obtener valor funcional
        return self.model.getObjVal()

    def free(self):
        # Liberar los recursos
        self.model.freeProb()