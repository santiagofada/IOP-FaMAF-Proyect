import pyscipopt as ps
import itertools

class PermutationModel:
    def __init__(self, nteams, costs,entera=False, **kwargs) -> None:
        assert costs.shape == (nteams, nteams, nteams-1), "Incorrect dimensions"

        self.model = None
        self.nteams = nteams
        self.costs = costs

        self.teams = range(self.nteams)
        self.rounds = range(self.nteams - 1)
        self.permutations = list(itertools.permutations(self.teams))
        self.permutations = [p for p in itertools.permutations(self.teams) if
                             all(p[r] != i for r, i in enumerate(self.teams))]
        print("AAAAAAAAAAAAAAAAAAAa")
        print(len(self.permutations))
        self._build(entera, **kwargs)

    def _build(self,entera=False, **kwargs):
        assert self.model is None, "Modelo ya inicializado"

        self.vars = {}
        self.model = ps.Model(f"Minimize carry-over effect for {self.nteams} teams", enablepricing=False)
        self.model.redirectOutput()
        self.model.setParam("display/freq", 1)

        # variables
        for i in self.teams:
            for pi in self.permutations:
                if entera:
                    var = self.model.addVar(name=f"z[{i},{pi}]", vtype="B")
                else:
                    var = self.model.addVar(name=f"z[{i},{pi}]", vtype="C")

                self.vars[i, pi] = var


        # Funcion objetivo
        self.model.setObjective(
            0.5 * ps.quicksum(
                self.costs[i, pi[r], r] * self.vars[i, pi] for i in self.teams for pi in self.permutations for r in self.rounds),
            sense="minimize"
        )



        # Restricciones
        # P.2 Cada ya¡ba equoi tiene una unica permutacion
        for i in self.teams:
            self.model.addCons(ps.quicksum(self.vars[i, pi] for pi in self.permutations) == 1)

        # P.3 se cumple a reflexion (i,j,r)) si y solo si ((j,i),r)
        for i, j in itertools.combinations(self.teams, 2):
            for r in self.rounds:
                lhs = ps.quicksum(self.vars[i, pi] for pi in self.permutations if pi[r] == j)
                rhs = ps.quicksum(self.vars[j, pi] for pi in self.permutations if pi[r] == i)
                self.model.addCons(lhs == rhs)

    def optimize(self):
        self.model.optimize()
        self.model.printStatistics()

    def get_objval(self):
        # Obtener valor funcional
        return self.model.getObjVal()

    def free(self):
        # Liberar los recursos
        self.model.freeProb()