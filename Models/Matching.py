import pyscipopt as ps
import itertools
from Utils.Matchingutils.pricer import RoundMatchingPricer
from Models.BaseModel import BaseModel


class MatchingModel(BaseModel):

    def _build(self, entera):
        self.model = ps.Model(f"Minimize carry-over effect for {self.nteams} teams", enablepricing=False)
        #self.model.redirectOutput()
        #self.model.setParam("display/freq", 1)
        self.model.hideOutput()

        teams = range(self.nteams)
        rounds = range(self.nrounds)
        matches = list(itertools.combinations(teams, r=2))

        # Variables
        self.var = [[] for _ in rounds]

        # Objective
        self.model.setObjective(
            0.0,
            sense="minimize"
        )

        # Restricciones
        # M2. un matching por ronda
        round_constrs = {
            r: self.model.addCons(
                ps.quicksum([]) == 1,
                modifiable=True
            )
            for r in rounds
        }
        # M3. Los equipos se cruzan una unica vez
        match_constrs = {
            m: self.model.addCons(
                ps.quicksum([]) == 1,
                modifiable=True
            )
            for m in matches
        }

        # Introduce pricer
        pricer = self.pricer = RoundMatchingPricer(self.nteams, self.var, (round_constrs, match_constrs), self.costs,entera=entera)
        self.model.includePricer(pricer, "RoundMatchingPricer", "A pricer for generating round schedules.")


    def get_nonzero_vars(self):
        seen = set()
        non_zero_vars = []
        for round_sched in self.var:
            for match in round_sched:
                var = match.get_var()
                value = self.model.getVal(var)
                if abs(value) > 1e-6 and var.name not in seen:
                    non_zero_vars.append((var.name, value))
                    seen.add(var.name)
        return non_zero_vars