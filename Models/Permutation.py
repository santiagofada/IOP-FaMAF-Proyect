import pyscipopt as ps
import itertools
from Models.BaseModel import BaseModel

class PermutationModel(BaseModel):

    def _build(self,entera=False, **kwargs):
        self.model = ps.Model(f"Minimize carry-over effect for {self.nteams} teams", enablepricing=False)
        self.model.hideOutput()

        teams = range(self.nteams)
        rounds = range(self.nrounds)

        combinations = list(itertools.combinations(teams, self.nteams - 1))
        permutations = []
        for combination in combinations:
            permu = list(itertools.permutations(combination))
            permutations.extend(permu)

        self.permutations = permutations

        # variables
        self.var = {}
        for i in teams:
            for pi in self.permutations:
                if i not in pi:
                    var_name = f"z[{i},{pi}]"
                    if entera:
                        var_type = "B"
                    else:
                        var_type = "C"

                    self.var[i, pi] = self.model.addVar(name=var_name, vtype=var_type)



        # Funcion objetivo
        self.model.setObjective(
            0.5 * ps.quicksum(
                self.costs[i, pi[r], r] * self.var[i, pi]
                for i in teams
                for pi in self.permutations if i not in pi
                for r in rounds),
            sense="minimize"
        )



        # Restricciones
        # P.2 Cada ya¡ba equoi tiene una unica permutacion
        for i in teams:
            self.model.addCons(
                ps.quicksum(self.var[i, pi] for pi in self.permutations if i not in pi) == 1
            )

        # P.3 se cumple a reflexion (i,j,r)) si y solo si ((j,i),r)
        for i, j in itertools.combinations(teams, 2):
            for r in rounds:
                lhs = ps.quicksum(self.var[i, pi] for pi in self.permutations if i not in pi and pi[r] == j)
                rhs = ps.quicksum(self.var[j, pi] for pi in self.permutations if j not in pi and pi[r] == i)
                self.model.addCons(lhs == rhs)


    def get_nonzero_vars(self):
        non_zero_vars = []
        for (i, pi), var in self.var.items():
            value = self.model.getVal(var)
            if value != 0:
                var_name = f"z[{i},{pi}]"
                non_zero_vars.append((var_name, value))
        return non_zero_vars
