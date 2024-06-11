import pyscipopt as ps
import itertools
import numpy as np
from Utils.util import sort_match
from Models.BaseModel import BaseModel


class TraditionalModel(BaseModel):

    def _build(self, entera=False):
        assert self.model is None, "Modelo ya inicializado"

        self.model = ps.Model(f"Minimize carry-over effect for {self.nteams} teams", enablepricing=False)
        #self.model.redirectOutput()
        #self.model.setParam("display/freq", 1)
        self.model.hideOutput()

        teams = range(self.nteams)
        rounds = range(self.nrounds)
        matches = list(itertools.combinations(teams, r=2))

        # variables X
        """
        self.var = {
            ((i, j), r): self.model.addVar(
                name=f"x[({i},{j}),{r}]",
                lb=0.0,
                ub=1.0,
                vtype=("B" if entera else "C")
            )
            for ((i, j), r) in itertools.product(matches, rounds)
        }
        """
        if entera:
            # variables enteras
            self.var = {
                ((i, j), r): self.model.addVar(name=f"x[({i},{j}),{r}]", lb=0.0, ub=1.0,
                                               vtype=("B"))
                for ((i, j), r) in itertools.product(matches, rounds)
            }
        else:
            # variables reales
            self.var = {
                ((i, j), r): self.model.addVar(name=f"x[{i},{j},{r + 1}]", lb=0.0, ub=1.0,
                                               vtype=("C"))
                for (i, j), r in itertools.product(matches, rounds)
            }

        # Funcion objetivo c_{m,r} * x_{m,r}
        self.model.setObjective(
            ps.quicksum(
                cost * self.var[(i, j), r]
                for (i, j, r), cost in np.ndenumerate(self.costs)
                if np.abs(cost) > 1e-6 and i < j
            ),
            sense="minimize"
        )

        # Restricciones

        # T2. Un partido se juega una unica vez
        for (i, j) in matches:
            self.model.addCons(
                ps.quicksum(self.var[(i, j), r] for r in rounds) == 1
            )

        # T3.  un partido solo se puede jugar una unica vez por ronda
        for i, r in itertools.product(teams, rounds):
            self.model.addCons(
                ps.quicksum(self.var[sort_match(i, j), r] for j in teams if i != j) == 1
            )


    def get_nonzero_vars(self):
        non_zero_vars = []
        for var in self.var.values():
            value = self.model.getVal(var)
            if abs(value) > 1e-6:
                non_zero_vars.append((var.name, value))
        return non_zero_vars